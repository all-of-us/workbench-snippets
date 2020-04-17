# Use snippet 'summarize_a_survey_module' to output a table and a graph of 
# participant counts by response for one question_concept_id
# The snippet assumes that a dataframe containing survey questions and answers already exists
# The snippet also assumes that setup has been run

# Update the next 3 lines
survey_df <- YOUR_SURVEY_df
question_concept_id <- 1585940
denominator <- NULL

####################################################################################
#                           DON'T CHANGE FROM HERE
####################################################################################
summarize_a_question_concept_id <- function(df, q_concept_id, denominator=NULL){
    df <- df %>% filter(question_concept_id == q_concept_id)
    
    new_df <- df %>% group_by(answer_concept_id, answer) %>%
                    summarize(n_participant = n_distinct(person_id)) %>%
                    ungroup() %>%
                    mutate(answer_concept_id = as.integer(answer_concept_id))
    if (!is.null(denominator)) {
        new_df <- new_df %>% mutate(response_rate = paste0(round(100*n_participant/denominator,2),'%'))
    }
    
    if (q_concept_id %in% as.vector(unique(df[['question_concept_id']]))){
        question_name <- as.vector(unique(df$question))
        print(str_glue("Distribution of response to {question_name}"))
        
        # show table
        print(new_df)

        # show graph
        options(repr.plot.width=12, repr.plot.height=6)
        ggplot(new_df) +
            geom_bar(aes(x=answer, y=n_participant), stat='identity') +
            coord_flip() +
            labs(y="Participant count", x="") +
            theme_minimal()
    }
    else {
        print("There is an error with your question_concept_id")
    }
}

summarize_a_question_concept_id(survey_df, question_concept_id, denominator)


