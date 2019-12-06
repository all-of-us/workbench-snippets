!pip -q install --user google.cloud.storage
# Imports useful library
from google.cloud import storage
import os

def copy_dataframe_to_bucket(source_dataframe, filename):   
    # store the dataframe in current workspace
    source_dataframe.to_csv(filename, index=False)
    
    # Get access to the bucket related to the current workspace
    my_storage = storage.Client()
    bucket_name = os.getenv('WORKSPACE_BUCKET').split('//')[1]
    my_bucket = my_storage.get_bucket(bucket_name)
    blob = my_bucket.blob(filename)
    
    # copy file from current workspace to the bucket
    blob.upload_from_filename(filename)
    print(f'[INFO] {filename} is successfully uploaded to your google bucket')

# Replace df with THE NAME OF YOUR DATAFRAME
my_dataframe = df   

# Replace 'test.csv' with THE NAME of the file you're going to store in the bucket (don't delete the quotation marks)
destination_filename = 'test.csv'

copy_dataframe_to_bucket(my_dataframe, destination_filename)