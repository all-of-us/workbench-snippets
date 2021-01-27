# Use snippet 'summarize_a_survey_module' to print a table of participant counts by question in a module
# The snippet assumes that a dataframe containing survey questions and answers already exists

# Update the next 3 lines

survey_df <- YOUR_DATASET_NAME_survey_df
module_name <- 'The Basics'
denominator <- NULL

####################################################################################
#                           DON'T CHANGE FROM HERE
####################################################################################
summarize_a_module <- function(df, module=NULL, denominator=NULL) {
    if (!is.null(module)){
        df <- df %>% filter(tolower(survey) == tolower(module))
    }
    data <- df %>% group_by(survey, question_concept_id, question) %>%
               summarize(n_participant = n_distinct(person_id))
    if (!is.null(denominator)) {
        data <- data %>% mutate(response_rate = paste0(round(100*n_participant/denominator,2),'%'))
    }
    data
}

summarize_a_module(survey_df, module_name, denominator)

