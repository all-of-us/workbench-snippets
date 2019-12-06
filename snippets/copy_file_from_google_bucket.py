!pip -q install --user google.cloud.storage
# Imports useful library
from google.cloud import storage
import os
import pandas as pd

def copy_file_from_bucket(source_filename):
    """Load file from bucket into a pandas dataframe"""
    # Get access to the file in the bucket related to the current workspace
    my_storage = storage.Client()
    bucket_name = os.getenv('WORKSPACE_BUCKET').split('//')[1]
    my_bucket = my_storage.get_bucket(bucket_name)
    blob = my_bucket.blob(source_filename)
    
    # copy file from bucket to the current workspace 
    blob.download_to_filename(source_filename)
    print(f'[INFO] {source_filename} is successfully downloaded from the Bucket.')
    return pd.read_csv(source_filename)

# replace 'test.csv' with the name of the file in your google bucket (don't delete the quotation marks)
name_of_file_in_bucket = 'test.csv'

# Load the file into a dataframe
my_dataframe = copy_file_from_bucket(name_of_file_in_bucket)
my_dataframe.head()