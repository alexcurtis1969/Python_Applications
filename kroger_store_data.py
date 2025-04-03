import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import seaborn as sns  # Import seaborn for enhanced visualizations
import boto3  # Import boto3 for AWS S3 interaction
import os  # Import os for operating system interactions
import hashlib  # Import hashlib for password hashing
import secrets  # Import secrets for generating secure tokens
from flask import Flask, render_template, request, send_from_directory, Response  # Import Flask for web application
from datetime import datetime, timedelta  # Import datetime for date/time operations
import schedule  # Import schedule for task scheduling
import time  # Import time for time-related operations
import logging  # Import logging for logging messages
import numpy as np  # Import numpy for numerical operations
import random  # Import random for random number generation
import matplotlib.ticker as ticker  # Import ticker for formatting axis ticks
import matplotlib.dates as mdates  # Import mdates for formatting date axis

# Kroger-Specific Configuration
S3_BUCKET_NAME = "kroger-sales-analysis-web"  # S3 bucket name
S3_FILE_NAME = "kroger_sales_analysis.csv"  # S3 file name
S3_VISUALIZATIONS_PREFIX = "kroger_sales_visualizations/"  # S3 prefix for visualizations
S3_REGION = "us-west-2"  # S3 region
CSV_FILE_PATH = "generic_store_data.csv"  # Local CSV file path
HTML_FILE_NAME = "index.html"  # HTML file name

PASSWORD_HASH = hashlib.sha256("kroger_web_password".encode()).hexdigest()  # Hash the password
SALT = secrets.token_hex(16)  # Generate a salt
PASSWORD_HASH = hashlib.sha256((PASSWORD_HASH + SALT).encode()).hexdigest()  # Hash the password with the salt

app = Flask(__name__)  # Initialize Flask app

# --- Data Generation Function ---

def generate_specific_store_data(num_days=90):
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]  # List of cities
    stores = [f"{city}_Store_{random.randint(1, 5)}" for city in cities for _ in range(2)]  # Generate store names
    categories = ["Electronics", "Clothing", "Groceries", "Home Goods", "Books", "Fuel"]  # List of product categories
    departments = ["Sales", "Marketing", "Inventory", "Customer Service"]  # List of departments
    fuel_types = ["Gasoline", "Diesel"]  # List of fuel types

    data = []  # Initialize data list
    start_date = datetime.now() - timedelta(days=num_days)  # Calculate start date

    for store in stores:
        for day in range(num_days):
            current_date = start_date  # Set current date
            for category in categories:
                for department in departments:
                    if category == "Electronics":
                        sales_amount = max(0, np.random.normal(loc=1500, scale=400))  # Generate sales amount
                    elif category == "Clothing":
                        sales_amount = max(0, np.random.normal(loc=1200, scale=350))  # Generate sales amount
                    elif category == "Groceries":
                        sales_amount = max(0, np.random.normal(loc=2000, scale=500))  # Generate sales amount
                    elif category == "Home Goods":
                        sales_amount = max(0, np.random.normal(loc=1000, scale=300))  # Generate sales amount
                    elif category == "Books":
                        sales_amount = max(0, np.random.normal(loc=800, scale=250))  # Generate sales amount
                    else:  # Fuel
                        gasoline_gallons = max(0, np.random.normal(loc=1000, scale=300))  # Generate gallons of gasoline
                        diesel_gallons = max(0, np.random.normal(loc=500, scale=150))  # Generate gallons of diesel
                        fuel_type = random.choice(fuel_types)  # Choose fuel type

                        base_gas_price = 3.8  # Base gasoline price
                        base_diesel_price = 4.2  # Base diesel price

                        week_of_year = current_date.isocalendar()[1]  # Get week of year
                        price_fluctuation = np.sin(week_of_year / 4) * 0.3  # Calculate price fluctuation

                        if fuel_type == "Gasoline":
                            if "New York" in store or "Los Angeles" in store:
                                regional_adjustment = 0.7  # Regional adjustment
                            elif "San Francisco" in store or "San Jose" in store:
                                regional_adjustment = 0.5  # Regional adjustment
                            else:
                                regional_adjustment = 0  # Regional adjustment
                        else:  # Diesel
                            if "New York" in store or "Los Angeles" in store:
                                regional_adjustment = 0.8  # Regional adjustment
                            elif "Houston" in store or "Dallas" in store:
                                regional_adjustment = 0.3  # Regional adjustment
                            else:
                                regional_adjustment = 0  # Regional adjustment

                        fuel_price = max(2.8, base_gas_price if fuel_type == "Gasoline" else base_diesel_price + price_fluctuation + regional_adjustment + np.random.normal(loc=0, scale=0.2 if fuel_type == "Gasoline" else 0.3))  # Calculate fuel price
                        gallons_sold = gasoline_gallons if fuel_type == "Gasoline" else diesel_gallons  # Get gallons sold

                        sales_amount = gallons_sold * fuel_price  # Calculate sales amount

                    if "New York" in store or "Los Angeles" in store:
                        sales_amount *= 1.2  # Adjust sales amount
                    elif "Chicago" in store or "Dallas" in store:
                        sales_amount *= 1.1  # Adjust sales amount
                    elif "San Jose" in store or "San Diego" in store:
                        sales_amount *= 1.05  # Adjust sales amount

                    if department == "Sales":
                        sales_amount *= 1.2  # Adjust sales amount
                    elif department == "Marketing":
                        sales_amount *= 0.8  # Adjust sales amount

                    if category == "Fuel":
                        data.append({
                            "store_id": store,
                            "sales_date": current_date.strftime("%Y-%m-%d"),
                            "product_category": category,
                            "department": department,
                            "sales_amount": sales_amount,
                            "gallons_sold": gallons_sold,
                            "fuel_type": fuel_type,
                            "fuel_price": fuel_price,
                        })

                    else:
                        data.append({
                            "store_id": store,
                            "sales_date": current_date.strftime("%Y-%m-%d"),
                            "product_category": category,
                            "department": department,
                            "sales_amount": sales_amount,
                            "gallons_sold": None,
                            "fuel_type": None,
                            "fuel_price": None,
                        })
            start_date += timedelta(days=1)  # Increment start date

    df = pd.DataFrame(data)  # Create DataFrame
    df.to_csv("generic_store_data.csv", index=False)  # Save DataFrame to CSV
    return df

# --- Analysis Functions (Kroger Sales Data) ---
def read_kroger_sales_data(csv_file):
    try:
        df = pd.read_csv(csv_file)  # Read CSV file
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]  # Clean column names
        logging.info(f"Read Kroger sales data: {csv_file} (Shape: {df.shape})")  # Log info
        return df
    except FileNotFoundError:
        logging.error(f"Kroger sales data file '{csv_file}' not found.")  # Log error
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Failed to read Kroger sales data '{csv_file}': {e}")  # Log error
        return pd.DataFrame()

def analyze_kroger_sales(df):
    analysis = {}
    if df.empty:
        logging.error("Kroger sales data is empty. Analysis aborted.")  # Log error
        return analysis

    store_id_col = "store_id"  # Store ID column
    department_col = "department"  # Department column
    category_col = "product_category"  # Category column
    sales_col = "sales_amount"  # Sales column
    date_col = "sales_date"  # Date column
    fuel_price_col = "fuel_price"  # Fuel price column
    gallons_sold_col = "gallons_sold"  # Gallons sold column
    fuel_type_col = "fuel_type"  # Fuel type column

    df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')  # Convert sales to numeric
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')  # Convert date to datetime

    analysis["total_sales"] = df[sales_col].sum()  # Calculate total sales
    analysis["avg_sales_per_store"] = df.groupby(store_id_col)[sales_col].mean().to_dict()  # Calculate average sales per store
    analysis["total_sales_per_department"] = df.groupby(department_col)[sales_col].sum().to_dict()  # Calculate total sales per department
    analysis["total_sales_per_category"] = df.groupby(category_col)[sales_col].sum().to_dict()  # Calculate total sales per category
    analysis["daily_sales_trend"] = df.groupby(df[date_col].dt.date)[sales_col].sum().to_dict()  # Calculate daily sales trend

    fuel_df = df[df[category_col] == "Fuel"]  # Filter fuel data
    if not fuel_df.empty:
        analysis["total_fuel_sales"] = fuel_df[sales_col].sum()  # Calculate total fuel sales
        analysis["avg_fuel_price"] = fuel_df[fuel_price_col].mean()  # Calculate average fuel price
        analysis["total_gallons_sold"] = fuel_df[gallons_sold_col].sum()  # Calculate total gallons sold
        analysis["gallons_sold_by_type"] = fuel_df.groupby(fuel_type_col)[gallons_sold_col].sum().to_dict()  # Calculate gallons sold by fuel type

    return analysis

def generate_kroger_sales_visualizations(df):
    if df.empty:
        logging.warning("Kroger sales data is empty. Cannot generate visualizations.")  # Log warning
        return

    store_id_col = "store_id"
    department_col = "department"
    category_col = "product_category"
    sales_col = "sales_amount"
    date_col = "sales_date"

    df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Average Sales Amount per Store Chart (Improved - Colored)
    plt.figure(figsize=(14, 8))  # Adjust figure size for better fit

    # Extract store locations (cities)
    df['city'] = df[store_id_col].apply(lambda x: x.split('_')[0])
    cities = df['city'].unique()

    # Create a color mapping for each city
    color_map = {city: plt.cm.get_cmap('viridis')(i / len(cities)) for i, city in enumerate(cities)}

    # Create bars with colors based on city
    for city in cities:
        city_data = df[df['city'] == city]
        plt.bar(city_data[store_id_col], city_data[sales_col], label=city, color=color_map[city])

    plt.title('Average Sales Amount per Store', y=1.05)
    plt.xlabel('Store')
    plt.ylabel('Sales Amount (USD)')
    plt.xticks(rotation=45, ha='right')

    # Add legend
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0.)

    plt.tight_layout(rect=[0, 0, 0.95, 1])  # Adjust layout to fit legend
    plt.savefig("sales_by_store.png")
    upload_to_s3("sales_by_store.png", S3_VISUALIZATIONS_PREFIX + "sales_by_store.png")
    plt.close()

    # Sales Trend Over Time Chart (Improved - Weekly Aggregation)
    plt.figure(figsize=(12, 6))
    weekly_sales = df.resample('W', on=date_col)[sales_col].sum()  # Aggregate to weekly sums
    ax = weekly_sales.plot()
    plt.title('Sales Trend Over Time', y=1.05)
    plt.xlabel('Date')
    plt.ylabel('Total Sales (USD)')

    # Format X-axis Dates (Weekly Intervals)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))  # Show weekly dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # Format dates as month-day
    plt.xticks(rotation=45, ha='right')  # Rotate labels

    # Format Y-axis with commas
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.tight_layout()
    plt.savefig("sales_trend.png")
    upload_to_s3("sales_trend.png", S3_VISUALIZATIONS_PREFIX + "sales_trend.png")
    plt.close()

    # Total Sales by Category Chart (Improved)
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=category_col, y=sales_col, data=df, estimator=sum, color='royalblue')
    plt.title('Total Sales by Category', y=1.05)
    plt.xlabel('Product Category')
    plt.ylabel('Total Sales (USD)')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    plt.savefig("sales_by_category.png")
    upload_to_s3("sales_by_category.png", S3_VISUALIZATIONS_PREFIX + "sales_by_category.png")
    plt.close()

    # Highest Sales by Region Chart (Improved)
    plt.figure(figsize=(14, 8))  # Adjust figure size for better fit
    df['city'] = df['store_id'].apply(lambda x: x.split('_')[0])
    region_sales = df.groupby(['city', 'product_category'])[sales_col].sum().reset_index()
    top_categories = region_sales.groupby('city').apply(lambda x: x.nlargest(2, sales_col)).reset_index(drop=True)

    # Use grouped bar chart
    sns.barplot(x='city', y=sales_col, hue='product_category', data=top_categories, palette='viridis')  # Use 'viridis' palette

    plt.title('Top 2 Sales by Region', y=1.05)
    plt.xlabel('City')  # Change x-axis label to 'City'
    plt.ylabel('Total Sales (USD)')
    plt.xticks(rotation=45, ha='right')

    # Move legend outside the chart
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0.)

    plt.tight_layout(rect=[0, 0, 0.95, 1])  # Adjust layout to fit legend
    plt.savefig("sales_by_region.png")
    upload_to_s3("sales_by_region.png", S3_VISUALIZATIONS_PREFIX + "sales_by_region.png")
    plt.close()

def generate_static_html(analysis_results):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kroger Sales Analysis</title>
        <style>
            body {{
                font-family: sans-serif;
                margin: 20px;
            }}
            h1 {{
                text-align: center;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            .number {{
                text-align: right;
            }}
            .bar-chart {{
                width: 80%;
                margin: 20px auto;
            }}
            .bar-chart img {{
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <h1>Kroger Sales Analysis (Last 90 Days)</h1>

        <div class="section">
            <h2>Total Sales</h2>
            <p><b>${analysis_results.get('total_sales', 'N/A'):,.2f}</b></p>
        </div>

        <div class="section">
            <h2>Average Sales per Store</h2>
            <table>
                <tr>
                    <th>Store</th>
                    <th class="number">Average Sales (USD)</th>
                </tr>
                {''.join([f'<tr><td>{store}</td><td class="number">{sales:,.2f}</td></tr>' for store, sales in analysis_results.get('avg_sales_per_store', {}).items()])}
            </table>
        </div>

        <div class="section">
            <h2>Total Fuel Sales</h2>
            <p><b>{analysis_results.get('total_fuel_sales', 'N/A'):,.0f}</b></p>
        </div>

        <div class="section">
            <h2>Average Fuel Price</h2>
            <p><b>${analysis_results.get('avg_fuel_price', 'N/A'):,.2f}</b></p>
        </div>

        <div class="section">
            <h2>Total Gallons Sold</h2>
            <p><b>{analysis_results.get('total_gallons_sold', 'N/A'):,.0f}</b></p>
        </div>

        <div class="section">
            <div class="bar-chart">
                <h2>Average Sales Amount per Store</h2>
                <img src="{S3_VISUALIZATIONS_PREFIX}sales_by_store.png" alt="Average Sales Amount per Store">
            </div>
        </div>

        <div class="section">
            <div class="bar-chart">
                <h2>Sales Trend Over Time</h2>
                <img src="{S3_VISUALIZATIONS_PREFIX}sales_trend.png" alt="Sales Trend Over Time">
            </div>
        </div>

        <div class="section">
            <div class="bar-chart">
                <h2>Total Sales by Category</h2>
                <img src="{S3_VISUALIZATIONS_PREFIX}sales_by_category.png" alt="Total Sales by Category">
            </div>
        </div>

        <div class="section">
            <div class="bar-chart">
                <h2>Top 2 Sales by Region</h2>
                <img src="{S3_VISUALIZATIONS_PREFIX}sales_by_region.png" alt="Top 2 Sales by Region">
            </div>
        </div>

    </body>
    </html>
    """
    with open(HTML_FILE_NAME, "w") as f:
        f.write(html_content)

def upload_static_html_to_s3():
    s3 = boto3.client("s3", region_name=S3_REGION)  # Initialize S3 client
    s3.upload_file(HTML_FILE_NAME, S3_BUCKET_NAME, HTML_FILE_NAME, ExtraArgs={'ContentType': 'text/html'})  # Upload HTML file
    logging.info(f"Uploaded {HTML_FILE_NAME} to S3 bucket: {S3_BUCKET_NAME}")  # Log info

def process_and_upload():
    df = generate_specific_store_data()  # Generate store data
    analysis_results = analyze_kroger_sales(df)  # Analyze sales data
    generate_kroger_sales_visualizations(df)  # Generate visualizations
    generate_static_html(analysis_results)  # Generate HTML
    upload_static_html_to_s3()  # Upload HTML to S3

def scheduled_task():
    process_and_upload()  # Process and upload data
    logging.info("Scheduled task completed.")  # Log info
    print_website_url()  # Print website URL

def print_website_url():
    s3_client = boto3.client('s3', region_name=S3_REGION)  # Initialize S3 client
    try:
        response = s3_client.get_bucket_website(Bucket=S3_BUCKET_NAME)  # Get website configuration
        print(f"Full Response: {response}")  # Print response
        if 'WebsiteConfiguration' in response:
            website_configuration = response['WebsiteConfiguration']  # Get website configuration
            if 'IndexDocument' in website_configuration:
                website_url = f"http://{S3_BUCKET_NAME}.s3-website-{S3_REGION}.amazonaws.com"  # Construct website URL
                print(f"Website URL: {website_url}")  # Print website URL
            else:
                print("Static website hosting is not properly configured for this bucket.")  # Print error message
        else:
            if 'IndexDocument' in response:
                website_url = f"http://{S3_BUCKET_NAME}.s3-website-{S3_REGION}.amazonaws.com"  # Construct website URL
                print(f"Website URL: {website_url}")  # Print website URL
            else:
                print("Static website hosting is not enabled for this bucket.")  # Print error message
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchWebsiteConfiguration':
            print("Static website hosting is not enabled for this bucket.")  # Print error message
        else:
            print(f"An error occurred: {e}")  # Print error message

def upload_to_s3(filename, s3_filename):
    s3 = boto3.client("s3", region_name=S3_REGION)  # Initialize S3 client
    s3.upload_file(filename, S3_BUCKET_NAME, s3_filename)  # Upload file to S3
    logging.info(f"Uploaded {filename} to S3 bucket: {S3_BUCKET_NAME}/{s3_filename}")  # Log info

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Configure logging
    scheduled_task()  # Run scheduled task once
    schedule.every(6).hours.do(scheduled_task)  # Schedule task to run every 6 hours
    logging.info("Scheduled task set to run every 6 hours.")  # Log info
    while True:
        schedule.run_pending()  # Run pending scheduled tasks
        time.sleep(60)  # Sleep for 60 seconds