# This snippet assumes you run setup first

# This code copies file in your Google Bucket and loads it into a dataframe

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
args = ["gsutil", "cp", f"{my_bucket}/data/{name_of_file_in_bucket}", "."]
output = subprocess.run(args, capture_output=True)

if output.returncode != 0:
    # failed to copy the file - add appropriate error handling here
    print(output.stderr)
else:
    print(f'[INFO] {name_of_file_in_bucket} is successfully downloaded into your working space')
    my_dataframe = pd.read_csv(name_of_file_in_bucket)
    my_dataframe.head()
