lapply(c('viridis', 'ggthemes', 'skimr'),
       function(pkg_name) { if(! pkg_name %in% installed.packages()) { install.packages(pkg_name)} } )

library(viridis)    # A nice color scheme for plots.
library(ggthemes)   # Common themes to change the look and feel of plots.
library(scales)     # Graphical scales map data to aesthetics in plots.
library(skimr)      # Better summaries of data.
library(lubridate)  # Date library from the tidyverse.
library(bigrquery)  # BigQuery R client.
library(tidyverse)  # Data wrangling packages.

## BigQuery setup.
BILLING_PROJECT_ID <- Sys.getenv('GOOGLE_PROJECT')
# Get the BigQuery curated dataset for the current workspace context.
CDR <- system(paste0("echo ",
    "$(jq -r '.CDR_VERSION_CLOUD_PROJECT' .all_of_us_config.json).",
    "$(jq -r '.CDR_VERSION_BIGQUERY_DATASET' .all_of_us_config.json)"),
    intern = TRUE)


## Plot setup.
theme_set(theme_bw(base_size = 14)) # Default theme for plots.

#' Returns a data frame with a y position and a label, for use annotating ggplot boxplots.
#'
#' @param d A data frame.
#' @return A data frame with column y as max and column label as length.
get_boxplot_fun_data <- function(df) {
  return(data.frame(y = max(df), label = stringr::str_c('N = ', length(df))))
}

## ---------------[ CHANGE THESE AS NEEDED] ---------------------------------------
# Set default parameter values so that all snippets run successfully with no edits needed.
COHORT_QUERY <- str_glue('SELECT person_id FROM `{CDR}.person`')  # Default to all participants.
MEASUREMENT_OF_INTEREST <- 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID <- 3000963        # Hemoglobin
UNIT_CONCEPT_ID <- 8713                  # gram per deciliter
MEASUREMENT_NAME <- '<this should be the measurement name>'
UNIT_NAME <- '<this should be the unit name>'
