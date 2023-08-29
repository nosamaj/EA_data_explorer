import boto3

# Set up S3 client for Linode object storage
s3 = boto3.client(
    "s3",
    endpoint_url="https://eu-central-1.linodeobjects.com",
    aws_access_key_id="",
    aws_secret_access_key="",
)

# List all objects in t
# 7480.he bucket



# Get the bucket name
bucket_name = 'bellas-horde'

# Get the prefix
prefix = 'EAData'
# Specify the local directory to download to
local_directory = '/home/nosamaj/EAdata'

# List objects in the specified prefix
objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Download each object
for obj in objects.get('Contents', []):
    key = obj['Key']
    if key.endswith('.parquet'):
        local_path = os.path.join(local_directory, os.path.basename(key))
        
        # Download the object
        s3.download_file(bucket_name, key, local_path)
        print(f'Downloaded: {key} to {local_path}')