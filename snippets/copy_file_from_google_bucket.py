import os
import pandas as pd

# Replace 'test.csv' with THE NAME of the file you're going to download from the bucket (don't delete the quotation marks)
name_of_file_in_bucket = 'test.csv'

########################################################################
##
################# DON'T CHANGE FROM HERE ###############################
##
########################################################################

# get the bucket name
my_bucket = os.getenv('WORKSPACE_BUCKET')

# copy csv file from the bucket to the current working space
!gsutil cp '{my_bucket}/{name_of_file_in_bucket}' .

print(f'[INFO] {name_of_file_in_bucket} is successfully downloaded into your working space')
# save dataframe in a csv file in the same workspace as the notebook
my_dataframe = read_csv(name_of_file_in_bucket)
my_dataframe.head()
    