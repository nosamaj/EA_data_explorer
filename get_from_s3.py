import boto3

# Set up S3 client for Linode object storage
s3 = boto3.client(
    "s3",
    endpoint_url="https://your-bucket-name.your-region.linodeobjects.com",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
)

# List all objects in t
# 7480.he bucket
response = s3.list_objects(Bucket="your-bucket-name")
for obj in response["Contents"]:
    print(obj["Key"])

import boto3
import re
from datetime import datetime

# Set up S3 client
s3 = boto3.client("s3")

# Set up bucket name and prefix
bucket_name = "your_bucket_name"
prefix = "your_prefix"

# Get list of all objects in bucket with specified prefix
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Define regular expression pattern for filename (dd-mm-yyyy)
pattern = re.compile(r"\d{2}-\d{2}-\d{4}")

# Loop through objects and download files with matching pattern
for obj in objects["Contents"]:
    filename = obj["Key"]
    match = re.search(pattern, filename)
    if match:
        # Convert matched string to datetime object
        dt = datetime.strptime(match.group(), "%d-%m-%Y")
        # Download object if filename matches pattern
        s3.download_file(bucket_name, filename, f'{dt.strftime("%Y-%m-%d")}.txt')
