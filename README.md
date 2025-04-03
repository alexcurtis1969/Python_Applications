# Kroger Sales Analysis Dashboard

This project generates and displays sales analysis visualizations for Kroger stores, including:

* **Average Sales Amount per Store:** Bar chart showing the average sales for each store, with each store location represented by a distinct color.
* **Sales Trend Over Time:** Line chart showing the weekly sales trend.
* **Total Sales by Category:** Bar chart showing the total sales for each product category.
* **Top 2 Sales by Region:** Grouped bar chart showing the top 2 selling product categories for each region.

The visualizations and analysis are generated from simulated sales data and uploaded to an AWS S3 bucket for web display.

## Prerequisites

* Python 3.x
* AWS account with S3 access
* Boto3 library (`pip install boto3`)
* Pandas library (`pip install pandas`)
* Matplotlib library (`pip install matplotlib`)
* Seaborn library (`pip install seaborn`)
* Flask library (`pip install Flask`)
* Schedule library (`pip install schedule`)

## Setup

1.  **AWS Configuration:**
    * Create an S3 bucket (e.g., `kroger-sales-analysis-web`).
    * Ensure your AWS credentials are configured correctly (e.g., via environment variables or AWS CLI).
    * Enable static website hosting for the S3 bucket.
    * Update the following variables in the code:
        * `S3_BUCKET_NAME`: Your S3 bucket name.
        * `S3_REGION`: Your AWS region.

2.  **Python Libraries:**
    * Install the required Python libraries using pip:
        ```bash
        pip install boto3 pandas matplotlib seaborn Flask schedule
        ```

3.  **Code Configuration:**
    * Optionally, modify the `generate_specific_store_data` function to customize the simulated sales data.
    * Set the `PASSWORD_HASH` and `SALT` variables if you want to implement basic password protection.

## Running the Code

1.  Execute the Python script:
    ```bash
    python your_script_name.py
    ```

2.  The script will:
    * Generate simulated sales data.
    * Analyze the sales data.
    * Create the visualizations.
    * Generate an HTML file (`index.html`) containing the visualizations.
    * Upload the visualizations and HTML file to the specified S3 bucket.
    * Print the S3 website URL to the console.

3.  The script is scheduled to run every 6 hours. You can modify the scheduling frequency by changing the `schedule.every(6).hours.do(scheduled_task)` line.

4.  Access the dashboard by opening the S3 website URL in your web browser.

## Code Structure

* `generate_specific_store_data(num_days=90)`: Generates simulated sales data for Kroger stores.
* `read_kroger_sales_data(csv_file)`: Reads sales data from a CSV file.
* `analyze_kroger_sales(df)`: Analyzes the sales data and returns analysis results.
* `generate_kroger_sales_visualizations(df)`: Generates the sales analysis visualizations.
* `generate_static_html(analysis_results)`: Generates the HTML content for the dashboard.
* `upload_static_html_to_s3()`: Uploads the HTML file to S3.
* `process_and_upload()`: Orchestrates the data generation, analysis, visualization, and upload process.
* `scheduled_task()`: Runs the `process_and_upload()` function and prints the website URL.
* `print_website_url()`: Prints the S3 website URL to the console.
* `upload_to_s3(filename, s3_filename)`: Uploads a file to S3.

## Notes

* This project uses simulated sales data. For real-world applications, you would replace the data generation with actual sales data from a database or other source.
* The visualizations are saved as PNG files and uploaded to S3.
* The HTML dashboard is generated dynamically and uploaded to S3.
* The script is scheduled to run periodically using the `schedule` library.
* Basic error handling and logging are included.

## Future Improvements

* Implement user authentication for the dashboard.
* Add more interactive visualizations using JavaScript libraries.
* Allow users to filter and customize the visualizations.
* Integrate with a real-time data source.
* Add more detailed analysis and metrics.
* Deploy the application using a serverless architecture (e.g., AWS Lambda and API Gateway).