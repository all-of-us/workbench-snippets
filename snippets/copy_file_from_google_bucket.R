library(tidyverse)

# replace 'test.csv' with the name of the file in your google bucket (don't delete the quotation marks)
name_of_file_in_bucket = 'test6.csv'

################ DO NOT CHANGE ANYTHING ABOVE THIS LINE ##############################
##########                                                           #################

# Get the bucket name
my_bucket <- Sys.getenv('WORKSPACE_BUCKET')

# Copy the file from current workspace to the bucket
system(paste0("gsutil cp ", my_bucket, "/", name_of_file_in_bucket, " ."), intern=T)

# Load the file into a dataframe
my_dataframe  <- read_csv(name_of_file_in_bucket)
head(my_dataframe)
