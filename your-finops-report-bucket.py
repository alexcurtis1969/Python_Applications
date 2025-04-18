import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-2"  # Updated to US East (Ohio)
BUCKET_NAME = "your-finops-report-bucket"  # Replace with your desired bucket name
INDEX_DOCUMENT = "index.html"
ERROR_DOCUMENT = "error.html"

s3_client = boto3.client('s3', region_name=AWS_REGION)

def create_s3_bucket(bucket_name, region):
    """Creates an S3 bucket if it doesn't exist."""
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"S3 bucket '{bucket_name}' created successfully in '{region}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"S3 bucket '{bucket_name}' already exists.")
        elif e.response['Error']['Code'] == 'BucketAlreadyExists':
            print(f"S3 bucket '{bucket_name}' already exists in another region.")
        else:
            print(f"Error creating S3 bucket '{bucket_name}': {e}")
            return False
    return True

def configure_static_website(bucket_name, index_doc, error_doc):
    """Configures the S3 bucket for static website hosting."""
    try:
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': index_doc},
                'ErrorDocument': {'Key': error_doc}
            }
        )
        print(f"Static website hosting configured for bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error configuring static website hosting for '{bucket_name}': {e}")
        return False
    return True

def set_bucket_policy(bucket_name):
    """Sets a bucket policy to allow public read access for website content."""
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }
    try:
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=str(policy)
        )
        print(f"Bucket policy set for public read access on '{bucket_name}'.")
    except ClientError as e:
        print(f"Error setting bucket policy for '{bucket_name}': {e}")
        return False
    return True

if __name__ == "__main__":
    if create_s3_bucket(BUCKET_NAME, AWS_REGION):
        configure_static_website(BUCKET_NAME, INDEX_DOCUMENT, ERROR_DOCUMENT)
        set_bucket_policy(BUCKET_NAME)
        website_endpoint = f"{BUCKET_NAME}.s3-website-{AWS_REGION}.amazonaws.com"
        print(f"\nYour static website endpoint: http://{website_endpoint}")
        print("Remember to upload your index.html (with password protection logic) and the FinOps report to the bucket.")
        print("Consider more secure password protection methods for sensitive data.")