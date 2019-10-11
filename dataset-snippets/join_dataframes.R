## -----[ CHANGE THE DATAFRAME NAME(S) TO MATCH YOURS FROM DATASET BUILDER] -----
measurement_df <- inner_join(YOUR_DATASET_NAME_person_df,
                             YOUR_DATASET_NAME_measurement_df) %>%
  mutate_if(is.list, as.character)  # Convert column type list as character.
  # TODO(workbench team): Remove the mutate_if after dataset builder switches from pandas-gbq to the bigrquery client.
