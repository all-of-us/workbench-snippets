# Use snippet 'add_age_to_demographics' to calculate the age of people in your demographics.
# It assumes the 'Setup' snippet has been executed.
# It also assumes that you got your demographics dataframe from Dataset Builder

# Note: This snippet calculates current age and does not take into account whether the person is already dead


## -----[ CHANGE THE DATAFRAME NAME(S) `YOUR_DATASET_NAME_person_df` TO MATCH YOURS FROM DATASET BUILDER] -----
YOUR_DATASET_NAME_person_df <- YOUR_DATASET_NAME_person_df %>%
                mutate_if(is.list, as.character) %>%
                mutate(age = year(today()) - year(YOUR_DATASET_NAME_person_df$date_of_birth))
