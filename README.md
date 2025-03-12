# AWS FinOps Cost Optimization Script

This Python script automates the process of loading AWS Cost and Usage Report (CUR) data from an S3 bucket, analyzing it, and generating FinOps cost optimization recommendations.

## Prerequisites

Before running this script, ensure you have the following:

-   **Python 3.6+:** Python is required to execute the script.
-   **Boto3:** The AWS SDK for Python, used to interact with AWS services. Install it using:
    ```bash
    pip install boto3
    ```
-   **Pandas:** A data manipulation library for Python, used to process the CUR data. Install it using:
    ```bash
    pip install pandas
    ```
-   **AWS Credentials:** Configure your AWS credentials with sufficient permissions to access the specified S3 bucket and retrieve the CUR file. You can configure credentials using the AWS CLI or environment variables.
-   **AWS CUR Data in S3:** You must have an AWS CUR CSV file stored in an S3 bucket.

## Setup Checklist

-   [ ] Install Python 3.6+
-   [ ] Install Boto3: `pip install boto3`
-   [ ] Install Pandas: `pip install pandas`
-   [ ] Configure AWS Credentials
-   [ ] Verify AWS CUR data exists in an S3 Bucket

## Setup

1.  **Clone the Repository (Optional):** If you have this code in a repository, clone it.

2.  **Install Dependencies:** Install the required Python packages as mentioned in the prerequisites.

3.  **Configure S3 Bucket and File:**
    -   Open the `script.py` file.
    -   Modify the following variables to match your S3 bucket and CUR file:
        ```python
        S3_BUCKET = "your-finops-data-bucket"
        CSV_FILE = "your_aws_cur.csv"
        ```
    -   Replace `"your-finops-data-bucket"` with the name of your S3 bucket.
    -   Replace `"your_aws_cur.csv"` with the name of your CUR CSV file.

## Usage

To run the script, execute the following command in your terminal:

```bash
python script.py