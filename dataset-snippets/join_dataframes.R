# Use snippet 'join_dataframes' to join together two dataframes.
# It assumes the 'Setup' snippet has been executed.
#
# In the example below, it joins Demographics '_person_df' and Measurements '_measurement_df' using
# any columns they have in common, which in this case should only be 'person_id'.
#
# See also https://dplyr.tidyverse.org/reference/join.html and https://r4ds.had.co.nz/relational-data.html#understanding-joins


## -----[ CHANGE THE DATAFRAME NAME(S) TO MATCH YOURS FROM DATASET BUILDER] -----
measurement_df <- inner_join(YOUR_DATASET_NAME_person_df,
                             YOUR_DATASET_NAME_measurement_df) %>%
  mutate_if(is.list, as.character)  # Convert column type list as character.

dim(measurement_df)
