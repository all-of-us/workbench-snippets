# This snippet assumes that you run setup first

# This code lists objects in your Google Bucket

# Get the bucket name
my_bucket = os.getenv('WORKSPACE_BUCKET')

# List objects in the bucket
print(subprocess.check_output(f"gsutil ls {my_bucket}", shell=True).decode('utf-8'))


