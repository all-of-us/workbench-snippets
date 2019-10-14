# Use snippet 'join_dataframes' to join together two dataframes.
# It assumes the 'Setup' snippet has been executed.
#
# In the example below, it joins Demographics '_person_df' and Measurements '_measurement_df' using
# any columns they have in common, which in this case should only be 'person_id'.
#
# See also https://pandas.pydata.org/pandas-docs/version/0.25.1/reference/api/pandas.merge.html


## -----[ CHANGE THE DATAFRAME NAME(S) TO MATCH YOURS FROM DATASET BUILDER] -----
measurement_df = pd.merge(left=YOUR_DATASET_NAME_person_df, right=YOUR_DATASET_NAME_measurement_df, how='inner')
