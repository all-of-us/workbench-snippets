# This snippet assumes that you run setup first

# This code lists objects in your Google Bucket

# Get the bucket name
my_bucket <- Sys.getenv('WORKSPACE_BUCKET')

# List objects in the bucket
system(paste0("gsutil ls ", my_bucket), intern=T)


