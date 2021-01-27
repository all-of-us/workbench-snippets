# Use snippet 'summarize_a_survey_module' to output a table and a graph of 
# participant counts by response for one question_concept_id
# The snippet assumes that a dataframe containing survey questions and answers already exists
# The snippet also assumes that setup has been run

# Update the next 3 lines
survey_df = YOUR_DATASET_NAME_survey_df
question_concept_id = 1585940
denominator = None # e.g: 200000

####################################################################################
#                           DON'T CHANGE FROM HERE
####################################################################################
def summarize_a_question_concept_id(df, question_concept_id, denominator=None):
    df = df.loc[df['question_concept_id'] == question_concept_id].copy()
    new_df = df.groupby(['answer_concept_id', 'answer'])['person_id']\
           .nunique()\
           .reset_index()\
           .rename(columns=dict(person_id='n_participant'))\
           .assign(answer_concept_id = lambda x: np.int32(x.answer_concept_id))
    if denominator:
        new_df['response_rate'] = round(100*new_df['n_participant']/denominator,2)
    if question_concept_id in df['question_concept_id'].unique():
        print(f"Distribution of response to {df.loc[df['question_concept_id'] == question_concept_id, 'question'].unique()[0]}")
        # show table
        display(new_df)
        # show graph
        display(ggplot(data=new_df) +
              geom_bar(aes(x='answer', y='n_participant'), stat='identity') +
               coord_flip() +
                labs(y="Participant count", x="") +
               theme_bw())
    else:
        print("There is an error with your question_concept_id")

summarize_a_question_concept_id(survey_df, question_concept_id, denominator)    


