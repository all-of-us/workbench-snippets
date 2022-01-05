library(tidyverse)
library(bigrquery)

# This query represents dataset "asdf" for domain "survey" and was generated for Synthetic Dataset in the Controlled Tier
dataset_15947426_survey_sql <- paste("
    SELECT
        answer.person_id,
        answer.survey_datetime,
        answer.survey,
        answer.question_concept_id,
        answer.question,
        answer.answer_concept_id,
        answer.answer,
        answer.survey_version_concept_id,
        answer.survey_version_name  
    FROM
        `ds_survey` answer   
    WHERE
        (
            question_concept_id IN (
                SELECT
                    DISTINCT(question_concept_id) as concept_id  
                FROM
                    `ds_survey` 
            )
        )  
AND (
            answer.PERSON_ID IN (
                SELECT
                    person_id  
                FROM
                    `cb_search_person` cb_search_person  
                WHERE
                    cb_search_person.person_id IN (
                        SELECT
                            person_id 
                        FROM
                            `cb_search_person` p 
                        WHERE
                            has_whole_genome_variant = 1 
                    ) 
                    AND cb_search_person.person_id IN (
                        SELECT
                            person_id 
                        FROM
                            `cb_search_person` p 
                        WHERE
                            DATE_DIFF(CURRENT_DATE,dob, YEAR) - IF(EXTRACT(MONTH 
                        FROM
                            dob)*100 + EXTRACT(DAY 
                        FROM
                            dob) > EXTRACT(MONTH 
                        FROM
                            CURRENT_DATE)*100 + EXTRACT(DAY 
                        FROM
                            CURRENT_DATE),
                            1,
                            0) BETWEEN 18 AND 24 
                            AND NOT EXISTS ( SELECT
                                'x' 
                            FROM
                                `death` d 
                            WHERE
                                d.person_id = p.person_id) ) 
                    )
                )
 ", sep="")

# Formuate a Cloud Storage destination path for the data exported from BigQuery.
# NOTE: By default data exported multiple times on the same day will overwrite older copies.
#       But data exported on a different days will write to a new location so that historical
#       copies can be kept as the dataset definition is changed.
survey_export_15947426_path <- file.path(
  Sys.getenv("WORKSPACE_BUCKET"),
  "bq_exports",
  Sys.getenv("OWNER_EMAIL"),
  strftime(lubridate::now(), "%Y%m%d"),  # Comment out this line if you want the export to always overwrite.
  "survey_15947426",
  "survey_15947426_*.csv")
message(str_glue('The data will be written to {survey_export_15947426_path}. Use this path when reading ',
                 'the data into your notebooks in the future.'))

# Perform the query and export the dataset to Cloud Storage as CSV files.
# NOTE: You only need to run `bq_table_save` once. After that, you can
#       just read data from the CSVs in Cloud Storage.
bq_table_save(
  bq_dataset_query(Sys.getenv("WORKSPACE_CDR"), dataset_15947426_survey_sql, billing = Sys.getenv("GOOGLE_PROJECT")),
  survey_export_15947426_path,
  destination_format = "CSV")

# Read the data directly from Cloud Storage into memory.
# NOTE: Alternatively you can `gsutil -m cp {survey_export_15947426_path}` to copy these files
#       to the Jupyter disk.
col_types <- NULL
dataset_15947426_survey_df <- bind_rows(
  map(system2('gsutil', args = c('ls', survey_export_15947426_path), stdout = TRUE, stderr = TRUE),
      function(csv) {
        message(str_glue('Loading {csv}.'))
        chunk <- read_csv(pipe(str_glue('gsutil cat {csv}')), col_types = col_types, show_col_types = FALSE)
        if (is.null(col_types)) {
          col_types <- spec(chunk)    
        }
        chunk
      })
)

dim(dataset_15947426_survey_df)

head(dataset_15947426_survey_df)
