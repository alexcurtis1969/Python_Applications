# Terraform FinOps Automation

This project automates the provisioning of an AWS S3 bucket using Terraform and integrates cost analysis using the AWS Cost Explorer API. It includes a Python script that orchestrates the Terraform workflow and retrieves cost data.

## Prerequisites

* **Terraform:** Install Terraform from [terraform.io](https://www.terraform.io/downloads.html).
* **Python 3:** Ensure you have Python 3 installed.
* **AWS CLI and Boto3:** Install the AWS CLI and Boto3 library:
    ```bash
    pip install awscli boto3
    ```
* **AWS Credentials:** Configure your AWS credentials using the AWS CLI or environment variables. Ensure the specified AWS profile in the script has the necessary permissions.

## Project Structure

Markdown

# Terraform FinOps Automation

This project automates the provisioning of an AWS S3 bucket using Terraform and integrates cost analysis using the AWS Cost Explorer API. It includes a Python script that orchestrates the Terraform workflow and retrieves cost data.

## Prerequisites

* **Terraform:** Install Terraform from [terraform.io](https://www.terraform.io/downloads.html).
* **Python 3:** Ensure you have Python 3 installed.
* **AWS CLI and Boto3:** Install the AWS CLI and Boto3 library:
    ```bash
    pip install awscli boto3
    ```
* **AWS Credentials:** Configure your AWS credentials using the AWS CLI or environment variables. Ensure the specified AWS profile in the script has the necessary permissions.

## Project Structure

terraform_finops_automation/
├── main.tf             # Terraform configuration for S3 bucket
├── terraform.tfvars    # Terraform variable definitions
├── terraform_finops_1.py # Python script for automation
└── README.md           # This file

## Setup and Usage

1.  **Configure Terraform Variables:**
    * Edit the `terraform.tfvars` file to set your desired AWS region and any other variables.
    * Example `terraform.tfvars`:

        ```terraform
        aws_region = "us-east-1"
        ```

2.  **Configure AWS Profile:**
    * Ensure that the `aws_profile_name` variable in the python script, matches an aws profile in your aws credentials file.

3.  **Run the Python Script:**
    * Execute the Python script to automate the process:

        ```bash
        python terraform_finops_1.py
        ```

    * The script will:
        * Initialize the Terraform project.
        * Generate a Terraform execution plan.
        * Display the estimated cost using AWS Cost Explorer.
        * Apply the Terraform plan to create the S3 bucket.
        * Output the S3 bucket ARN.

## Terraform Configuration (`main.tf`)

This file defines the AWS S3 bucket resource.

```terraform
resource "aws_s3_bucket" "example_bucket" {
  bucket = "my-unique-bucket-name-generated-by-python" #Ensure this name is globally unique
}

resource "aws_s3_bucket_acl" "example_bucket_acl" {
  bucket = aws_s3_bucket.example_bucket.id
  acl    = "private"
}

output "s3_bucket_arn" {
  value = aws_s3_bucket.example_bucket.arn
}
Python Script (terraform_finops_1.py)
This script automates the Terraform workflow and retrieves cost data.

Python

import os
import json
import subprocess
import boto3
from datetime import datetime, timedelta

# ... (Functions for Terraform commands and cost analysis)

def main():
    terraform_directory = "YOUR_TERRAFORM_DIRECTORY" #Change this to your terraform directory.
    var_file_path = "YOUR_TERRAFORM_VAR_FILE" #Change this to your terraform var file.
    aws_profile_name = "YOUR_AWS_PROFILE_NAME" #Change this to your aws profile name.

    # ... (Terraform and cost analysis workflow)

if __name__ == "__main__":
    main()

