if (!require('cloudml')) install.packages('cloudml')
library(cloudml)
library(tidyverse)

copy_file_from_bucket <- function(source_filename) {
    my_bucket <- Sys.getenv('WORKSPACE_BUCKET')
    
    # copy file from bucket to the current workspace
    gs_copy(paste0(my_bucket, '/', source_filename), source_filename)
    
    # read file into a dataframe
    my_dataframe <- read_csv(source_filename)
    cat('[INFO]', {source_filename}, 'is successfully downloaded from your google bucket.')
    
    return(my_dataframe)
}

################ DO NOT CHANGE ANYTHING ABOVE THIS LINE ##############################
##########                                                           #################

# replace 'test.csv' with the name of the file in your google bucket (don't delete the quotation marks)
name_of_file_in_bucket = 'test.csv'

# Load the file into a dataframe
my_dataframe = copy_file_from_bucket(name_of_file_in_bucket)
head(my_dataframe)