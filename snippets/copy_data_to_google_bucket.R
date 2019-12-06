if (!require('cloudml')) install.packages('cloudml')
library(cloudml)
library(tidyverse)

copy_data_to_google_bucket <- function(source_dataframe, filename) {
    # store the dataframe in current workspace
    write_excel_csv(source_dataframe, filename)
    
    my_bucket <- Sys.getenv('WORKSPACE_BUCKET')
    # copy file from current workspace to the bucket
    gs_copy(filename, my_bucket)
    cat('[INFO]', filename, "is successfully uploaded in your google bucket.")
}

################ DO NOT CHANGE ANYTHING ABOVE THIS LINE ##############################
##########                                                           #################

# Replace df with THE NAME OF YOUR DATAFRAME
my_dataframe <- df

# Replace 'test3.csv' with THE NAME of the file you're going to store in the bucket (don't delete the quotation marks)
destination_filename <- 'test3.csv'

copy_data_to_google_bucket(my_dataframe, destination_filename)