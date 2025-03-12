import boto3
import pandas as pd

# S3 Bucket Configuration: Define the S3 bucket name and the CSV file to load.
S3_BUCKET = "my-finops-data-bucket"
CSV_FILE = "sample_aws_cur.csv"

# Load AWS CUR Data from S3
def load_cur_data():
    # Create an S3 client to interact with AWS S3
    s3 = boto3.client("s3")
    
    # Fetch the object (CSV file) from the S3 bucket
    obj = s3.get_object(Bucket=S3_BUCKET, Key=CSV_FILE)
    
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(obj["Body"])

    # Convert the 'UsageDate' column to a datetime object for easier analysis
    df["UsageDate"] = pd.to_datetime(df["UsageDate"])
    
    # Return the processed DataFrame containing CUR data
    return df

# Generate FinOps Recommendations based on AWS service costs
def generate_recommendations(df):
    # Initialize an empty list to store the generated recommendations
    recommendations = []
    
    # Group data by service and calculate the average cost per service
    avg_costs = df.groupby("Service")["Cost"].mean().sort_values(ascending=False)
    
    # Loop through each service and generate optimization recommendations
    for service, avg_cost in avg_costs.items():
        # Check for each service and generate a recommendation for cost optimization
        if service == "EC2":
            recommendations.append(f"🚀 **EC2 Optimization:** Consider using **Reserved Instances (RI) or Spot Instances** to reduce costs.")
        elif service == "RDS":
            recommendations.append(f"💾 **RDS Optimization:** Evaluate **database instance size** and consider **Aurora Serverless** for scaling.")
        elif service == "S3":
            recommendations.append(f"🗄️ **S3 Optimization:** Use **Lifecycle Policies** to move infrequently accessed data to **Glacier or Intelligent-Tiering**.")
        elif service == "Lambda":
            recommendations.append(f"⚡ **Lambda Optimization:** Check for **over-provisioned memory** or redundant invocations to reduce execution costs.")
        elif service == "EKS":
            recommendations.append(f"📦 **EKS Optimization:** Ensure **right-sized worker nodes** and use **Cluster Autoscaler** to minimize unused capacity.")
    
    # Return the list of recommendations
    return recommendations

# Main execution block
if __name__ == "__main__":
    # Inform the user that the script is fetching AWS CUR data from S3
    print("🔄 Fetching AWS CUR Data from S3...")
    
    # Load the CUR data from S3
    cost_data = load_cur_data()
    
    # Inform the user that the recommendations are being generated
    print("💰 Generating FinOps Cost Optimization Recommendations...")
    
    # Generate the cost optimization recommendations based on the loaded data
    recommendations = generate_recommendations(cost_data)
    
    # Print each recommendation
    for rec in recommendations:
        print("✅", rec)
