# Use snippet 'add_age_to_demographics' to calculate the age of people in your demographics data
# It assumes the 'Setup' snippet has been executed.


## -----[ CHANGE THE DATAFRAME NAME(S) `YOUR_DATASET_NAME_person_df` TO MATCH YOURS FROM DATASET BUILDER] -----

DEATH_QUERIES = (
"SELECT "
"person_id, "
"death_date "
"FROM `{dataset}.death`"
"WHERE person_id in {pid}"
)

def get_death_df(person_id):
    """Extract death data related to @person_id
    
    Parameters:
        person_id: a list or pandas series
    Returns:
        Dataframe of death data
    """
    person_id = tuple(person_id)
    return pd.read_gbq(DEATH_QUERIES.format(dataset=CDR, pid=person_id), dialect='standard')

def add_age_to_person_df(person_df):
    """Calculate age of people in person_df dataframe
    
    Parameters:
        person_df: a dataframe
    Returns:
        Dataframe person_df with a new column `Age`
    """
    original_cols = person_df.columns.to_list()
    
    person_id = person_df['PERSON_ID']
    death_df = get_death_df(person_id)
    new_person_df = person_df.merge(death_df, left_on='PERSON_ID', right_on='person_id', how='left')
    
    # convert all dates into year
    this_year = pd.to_datetime('today').year
    new_person_df['dob'] = pd.to_datetime(new_person_df['DATE_OF_BIRTH']).dt.year
    new_person_df['death_year'] = pd.to_datetime(new_person_df['death_date']).dt.year
    
    # Age is age at death if the person is already dead, otherwise it is today's age
    new_person_df['AGE'] = np.where(new_person_df['death_date'].isnull(), 
                                    this_year - new_person_df['dob'],
                                    new_person_df['death_year'] - new_person_df['dob'])
    return new_person_df[original_cols + ['AGE']]

person_with_age_df = add_age_to_person_df(YOUR_DATASET_NAME_person_df)
person_with_age_df.shape

