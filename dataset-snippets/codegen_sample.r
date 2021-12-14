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

# Extract the cohort to Cloud Storage as CSV.
out_dir_15947426 <- "out_15947426"
export_15947426_glob <- paste(out_dir_15947426, "/export15947426-*.csv")
export_15947426_path <- paste(Sys.getenv("WORKSPACE_BUCKET"), "/bq_exports/", export_15947426_glob, sep="")
bq_table_save(
    bq_dataset_query(Sys.getenv("WORKSPACE_CDR"), dataset_15947426_survey_sql, billing=Sys.getenv("GOOGLE_PROJECT")),
    export_15947426_path,
    destination_format="CSV"
)

# Copy the CSV file(s) to the local VM file system.
dir.create(out_dir_15947426)
system2("gsutil", paste("-m", "cp", export_15947426_path, paste(out_dir_15947426, "/")), stdout=TRUE, stderr=TRUE)

# Load the local CSV file(s) as a data frame.
dataset_15947426_survey_df <- data.table::rbindlist(lapply(Sys.glob(export_15947426_glob), data.table::fread))

head(dataset_15947426_survey_df)
