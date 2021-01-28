# Use snippet 'summarize_a_survey_module' to print a table of participant counts by question in a module
# The snippet assumes that a dataframe containing survey questions and answers already exists

# Update the next 3 lines
survey_df = YOUR_DATASET_NAME_survey_df
module_name = 'The Basics' # e.g: 'The Basics', 'Lifestyle', 'Overall Health', etc.
denominator = None # e.g: 200000

####################################################################################
#                           DON'T CHANGE FROM HERE
####################################################################################

def summarize_a_module(df, module=None, denominator=None):
    if module:
        df = df[df['survey'].str.lower() == module.lower()].copy()
    data = (df.groupby(['survey','question_concept_id','question'])['person_id'].nunique()
                .reset_index()
                .rename(columns={'person_id':'n_participant'}))
    if denominator:
        data['response_rate'] = round(100*data['n_participant']/denominator,2)
    return data

summarize_a_module(df=survey_df, module=module_name, denominator=denominator)

