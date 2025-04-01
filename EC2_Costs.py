import matplotlib
matplotlib.use('Agg')  # Force Matplotlib to use the Agg backend for server-side image generation

import pandas as pd
import csv
import time
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import boto3
import os
import hashlib
import secrets
from flask import Flask, render_template, request, send_from_directory, Response

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS S3 Configuration
S3_BUCKET_NAME = "alexas-ec2-cost-analysis-bucket"  # Name of the S3 bucket
S3_FILE_NAME = "ec2_analysis.csv"  # Name of the CSV file in S3
S3_VISUALIZATIONS_PREFIX = "visualizations/"  # Prefix for visualization files in S3
S3_REGION = "us-east-1"  # AWS region for S3

# Password Protection
PASSWORD_HASH = hashlib.sha256("myStrongPassword123!".encode()).hexdigest()  # Hash of the password
SALT = secrets.token_hex(16)  # Generate a random salt
PASSWORD_HASH = hashlib.sha256((PASSWORD_HASH + SALT).encode()).hexdigest()  # Hash the password with the salt

# Flask App
app = Flask(__name__)

# --- Analysis Functions ---
def read_data_from_csv(csv_file):
    try:
        df = pd.read_csv(csv_file)  # Read CSV file into a Pandas DataFrame
        logging.info(f"Read CSV file: {csv_file} (Shape: {df.shape})")
        return df
    except FileNotFoundError:
        logging.error(f"CSV file '{csv_file}' not found.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Failed to read CSV '{csv_file}': {e}")
        return pd.DataFrame()

def analyze_ec2_costs(df):
    analysis = {}
    if df.empty:
        logging.error("DataFrame is empty for analysis. Analysis aborted.")
        return analysis

    df.columns = [str(col).strip().lower().replace(" ", "").replace("$", "").replace("(", "").replace(")", "").replace("%", "") for col in df.columns]  # Standardize column names
    logging.debug(f"Standardized DataFrame Columns: {df.columns.tolist()}")

    runtime_col = "runtimedays"
    recommendation_col = "recommendation"
    cost_col = "monthlycost"
    savings_col = "estimatedsavings"
    cpu_col = "avgcpu"

    analysis["total_ec2_running"] = len(df[df[runtime_col] > 0]) if runtime_col in df.columns else 0  # Count running EC2 instances
    analysis["total_ec2_not_running"] = len(df[df[runtime_col] == 0]) if runtime_col in df.columns else 0  # Count non-running EC2 instances

    cost_col_actual = next((col for col in df.columns if cost_col in col), None)  # Find the actual cost column
    if cost_col_actual:
        df[cost_col_actual] = pd.to_numeric(df[cost_col_actual].astype(str).replace(r'[$,]', '', regex=True), errors='coerce')  # Convert cost column to numeric
        analysis["total_cost_running"] = df[df[runtime_col] > 0][cost_col_actual].sum() if runtime_col in df.columns else 0  # Calculate total cost of running instances
        logging.debug(f"Calculated total cost of running EC2s: {analysis.get('total_cost_running', 0):.2f}")
    else:
        logging.warning(f"Column like '{cost_col}' not found for total cost analysis.")

    analysis["most_common_instance_types"] = df["instancetype"].value_counts().to_dict()  # Count instance types
    analysis["avg_cost_per_instance_type"] = df.groupby("instancetype")[cost_col_actual].mean().to_dict() if cost_col_actual else {}  # Calculate average cost per instance type
    analysis["avg_cpu_per_instance_type"] = df.groupby("instancetype")[cpu_col].mean().to_dict() if cpu_col in df.columns else {}  # Calculate average CPU per instance type
    analysis["total_cost_per_region"] = df.groupby("region")[cost_col_actual].sum().to_dict() if cost_col_actual else {}  # Calculate total cost per region

    low_utilization_instances = df[df[cpu_col] < 20] if cpu_col in df.columns else pd.DataFrame()  # Find low utilization instances
    high_utilization_instances = df[df[cpu_col] > 80] if cpu_col in df.columns else pd.DataFrame()  # Find high utilization instances
    analysis["low_utilization_percentage"] = (len(low_utilization_instances) / len(df)) * 100 if len(df) > 0 else 0  # Calculate low utilization percentage
    analysis["high_utilization_percentage"] = (len(high_utilization_instances) / len(df)) * 100 if len(df) > 0 else 0  # Calculate high utilization percentage
    analysis["recommendation_breakdown"] = df[recommendation_col].value_counts().to_dict() if recommendation_col in df.columns else {}  # Count recommendations

    savings_col_actual = next((col for col in df.columns if savings_col in col), None)  # Find the actual savings column
    if savings_col_actual and cost_col_actual:
        df[savings_col_actual] = pd.to_numeric(df[savings_col_actual].astype(str).replace(r'[$,]', '', regex=True), errors='coerce')  # Convert savings column to numeric
        analysis["total_cost_with_savings"] = analysis.get("total_cost_running", 0) - df[savings_col_actual].sum()  # Calculate total cost with savings
        logging.debug(f"Calculated total cost with savings: {analysis.get('total_cost_with_savings', 0):.2f}")
    else:
        analysis["total_cost_with_savings"] = analysis.get("total_cost_running", 0)

    if analysis.get("total_cost_running", 0) > 0 and savings_col_actual:
        analysis["potential_savings_percentage"] = (df[savings_col_actual].sum() / analysis["total_cost_running"]) * 100  # Calculate potential savings percentage
    else:
        analysis["potential_savings_percentage"] = 0

    return analysis

def save_analysis_results_to_csv(analysis_results, csv_filename="ec2_analysis.csv"):
    if not analysis_results:
        logging.info("No analysis results to save.")
        return

    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Metric", "Value"])

            def format_number(value, decimals=2):
                return "{:,.{}f}".format(value, decimals)

            def format_percentage(value, decimals=2):
                return "{:,.{}f}%".format(value, decimals)

            def format_currency(value, decimals=2):
                return "${:,.{}f}".format(value, decimals)

            def sort_dict_by_value(dictionary, reverse=True):
                return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse))

            for key, value in analysis_results.items():
                if isinstance(value, (int, float)):
                    if "cost" in key.lower():
                        writer.writerow([key, format_currency(value)])
                    elif "percentage" in key.lower():
                        writer.writerow([key, format_percentage(value)])
                    else:
                        writer.writerow([key, format_number(value)])
                elif isinstance(value, dict):
                    sorted_dict = sort_dict_by_value(value)
                    if "instance type" in key.lower():
                        top_n = 3
                        for sub_key, sub_value in list(sorted_dict.items())[:top_n]:
                            if "cost" in key.lower():
                                writer.writerow([f"Average Cost ({sub_key})", format_currency(sub_value)])
                            elif "cpu" in key.lower():
                                writer.writerow([f"Average CPU ({sub_key})", format_number(sub_value)])
                            else:
                                writer.writerow([f"Most Common Instance Type ({sub_key})", format_number(sub_value)])
                    elif "region" in key.lower():
                        for sub_key, sub_value in sorted_dict.items():
                            writer.writerow([f"Total Cost Per Region ({sub_key})", format_currency(sub_value)])
                    elif "recommendation" in key.lower():
                        for sub_key, sub_value in sorted_dict.items():
                            writer.writerow([f"Recommendation Breakdown ({sub_key})", format_number(sub_value)])
                else:
                    writer.writerow([key, str(value)])
        logging.info(f"Analysis results saved to '{csv_filename}'")
    except Exception as e:
        logging.error(f"Could not save analysis results to CSV '{csv_filename}': {e}")

def generate_visualizations(df):
    logging.info("generate_visualizations() called.")
    if df.empty:
        logging.warning("DataFrame is empty. Cannot generate visualizations.")
        return

    if not os.access(".", os.W_OK):  # Check write permissions
        logging.error("No write permissions in the current directory.")
        return

    df.columns = [str(col).strip().lower().replace(" ", "").replace("$", "").replace("(", "").replace(")", "").replace("%", "") for col in df.columns]  # Standardize column names
    print(f"DataFrame Columns after standardization: {df.columns}")

    if "instancetype" not in df.columns or "region" not in df.columns or "monthlycost" not in df.columns or "avgcpu" not in df.columns or "recommendation" not in df.columns:
        logging.error("Required columns not found in DataFrame after standardization. Cannot generate visualizations.")
        return

    plt.figure(figsize=(10, 6))
    sns.countplot(y="instancetype", data=df, order=df["instancetype"].value_counts().index[:10], palette="pastel", hue="instancetype", legend=False)
    try:
        print(f"local file exists: {os.path.exists('instance_type_distribution.png')}")
        plt.savefig("instance_type_distribution.png")
        logging.info("instance_type_distribution.png saved locally.")
        upload_to_s3("instance_type_distribution.png", S3_VISUALIZATIONS_PREFIX + "instance_type_distribution.png")
        logging.info("instance_type_distribution.png saved and uploaded successfully")
    except Exception as e:
        logging.error(f"Error saving/uploading instance_type_distribution.png: {e}")
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="region", y="monthlycost", data=df, estimator=sum, palette="viridis", hue="region", legend=False)
    try:
        print(f"local file exists: {os.path.exists('cost_per_region.png')}")
        plt.savefig("cost_per_region.png")
        logging.info("cost_per_region.png saved locally.")
        upload_to_s3("cost_per_region.png", S3_VISUALIZATIONS_PREFIX + "cost_per_region.png")
        logging.info("cost_per_region.png saved and uploaded successfully")
    except Exception as e:
        logging.error(f"Error saving/uploading cost_per_region.png: {e}")
        print(f"Error during cost_per_region saving: {e}")  # Added print statement for debugging
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.histplot(df["avgcpu"], bins=20, kde=True, color="skyblue")
    try:
        print(f"local file exists: {os.path.exists('cpu_utilization_distribution.png')}")
        plt.savefig("cpu_utilization_distribution.png")
        logging.info("cpu_utilization_distribution.png saved locally.")
        upload_to_s3("cpu_utilization_distribution.png", S3_VISUALIZATIONS_PREFIX + "cpu_utilization_distribution.png")
        logging.info("cpu_utilization_distribution.png saved and uploaded successfully")
    except Exception as e:
        logging.error(f"Error saving/uploading cpu_utilization_distribution.png: {e}")
        print(f"Error during cpu_utilization_distribution saving: {e}")  # Added print statement for debugging
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(x="recommendation", data=df, palette="Set2", hue="recommendation", legend=False)
    try:
        print(f"local file exists: {os.path.exists('recommendation_breakdown.png')}")
        plt.savefig("recommendation_breakdown.png")
        logging.info("recommendation_breakdown.png saved locally.")
        upload_to_s3("recommendation_breakdown.png", S3_VISUALIZATIONS_PREFIX + "recommendation_breakdown.png")
        logging.info("recommendation_breakdown.png saved and uploaded successfully")
    except Exception as e:
        logging.error(f"Error saving/uploading recommendation_breakdown.png: {e}")
    plt.close()

# --- S3 Upload Function ---
def upload_to_s3(file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3', region_name=S3_REGION)
    try:
        logging.info(f"Attempting to upload '{file_name}' to S3: {S3_BUCKET_NAME}/{object_name}")
        s3_client.upload_file(file_name, S3_BUCKET_NAME, object_name)
        logging.info(f"File '{file_name}' uploaded to S3: {S3_BUCKET_NAME}/{object_name}")
    except Exception as e:
        logging.error(f"Error uploading file '{file_name}' to S3: {e}")
        print(f"Upload error: {e}")
        print(f"File path that was attempted to upload: {file_name}")
        print(f"S3 path that was attempted to use: {S3_BUCKET_NAME}/{object_name}")

# --- S3 Bucket Creation ---
def create_s3_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)  # Create bucket in default region
        else:
            s3_client = boto3.client('s3', region_name=region)
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)  # No location constraint for us-east-1
            else:
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)  # Create bucket in specified region

        logging.info(f"S3 bucket '{bucket_name}' created successfully in region '{region or 'default'}'.")
        return True

    except Exception as e:
        logging.error(f"Error creating S3 bucket '{bucket_name}': {e}")
        return False

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        password_hash = hashlib.sha256((hashlib.sha256(password.encode()).hexdigest() + SALT).encode()).hexdigest()
        if password_hash == PASSWORD_HASH:
            return render_template("index.html")
        else:
            return "Incorrect password."
    return render_template("login.html")

@app.route("/download")
def download_file():
    s3_client = boto3.client('s3', region_name=S3_REGION)
    try:
        s3_client.download_file(S3_BUCKET_NAME, S3_FILE_NAME, "downloaded_ec2_analysis.csv")  # Download file from S3
        return send_from_directory(".", "downloaded_ec2_analysis.csv", as_attachment=True)
    except Exception as e:
        return f"Error downloading file: {e}"

@app.route("/visualizations/<filename>")
def get_visualization(filename):
    s3_client = boto3.client('s3', region_name=S3_REGION)
    local_filename = f"temp_{filename}"
    try:
        s3_client.download_file(S3_BUCKET_NAME, S3_VISUALIZATIONS_PREFIX + filename, local_filename)  # Download visualization from S3
        return send_from_directory(".", local_filename, as_attachment=False)
    except Exception as e:
        return f"Error downloading visualization: {e}"

@app.route("/run_analysis")
def run_analysis():
    print("run_analysis() called!")
    start_time = time.time()
    csv_file = "ec2_data.csv"
    df = read_data_from_csv(csv_file)

    if not df.empty:
        analysis_results = analyze_ec2_costs(df)
        save_analysis_results_to_csv(analysis_results)
        if os.path.exists("ec2_analysis.csv"):
            logging.info("ec2_analysis.csv exists locally.")
        else:
            logging.error("ec2_analysis.csv does not exist locally.")
        upload_to_s3("ec2_analysis.csv", S3_FILE_NAME)  # Upload analysis results to S3
        logging.info(f"Uploaded ec2_analysis.csv to S3")
        generate_visualizations(df)  # Generate and upload visualizations
        logging.info(f"Generated and uploaded visualizations to s3")
        if os.path.exists("instance_type_distribution.png"):
            logging.info("instance_type_distribution.png exists locally.")
        else:
            logging.error("instance_type_distribution.png does not exist locally.")
        if os.path.exists("cost_per_region.png"):
            logging.info("cost_per_region.png exists locally.")
        else:
            logging.error("cost_per_region.png does not exist locally.")
        if os.path.exists("cpu_utilization_distribution.png"):
            logging.info("cpu_utilization_distribution.png exists locally.")
        else:
            logging.error("cpu_utilization_distribution.png does not exist locally.")
        if os.path.exists("recommendation_breakdown.png"):
            logging.info("recommendation_breakdown.png exists locally.")
        else:
            logging.error("recommendation_breakdown.png does not exist locally.")
        return "Analysis completed and results uploaded to S3."
    else:
        return "Error: DataFrame is empty."

# --- Test S3 Connectivity ---
def test_s3_connectivity():
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)  # List objects in the S3 bucket
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"Object found in S3: {obj['Key']}")
        else:
            print("Bucket is empty.")
    except Exception as e:
        print(f"Error testing S3 connectivity: {e}")

if __name__ == "__main__":
    if create_s3_bucket(S3_BUCKET_NAME, S3_REGION):  # Create S3 bucket if it doesn't exist
        test_s3_connectivity()  # Test S3 connectivity
        app.run(debug=True)  # Run the Flask app
    else:
        print("S3 bucket creation failed. Application will not run.")