# Only install missing libraries, per https://stackoverflow.com/a/23286257/4138705.
install_if_missing <- function(packages) {
  if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
    install.packages(setdiff(packages, rownames(installed.packages())))
  }
}
install_if_missing(c('viridis', 'ggthemes', 'scales', 'skimr', 'lubridate', 'bigrquery', 'tidyverse'))

library(viridis)    # A nice color scheme for plots.
library(ggthemes)   # Common themes to change the look and feel of plots.
library(scales)     # Graphical scales map data to aesthetics in plots.
library(skimr)      # Better summaries of data.
library(lubridate)  # Date library from the tidyverse.
library(bigrquery)  # BigQuery R client.
library(tidyverse)  # Data wrangling packages.

# Get the BigQuery curated dataset for the current workspace context.
DATASET <- system(paste("echo ",
    "$(jq -r '.CDR_VERSION_CLOUD_PROJECT' .all_of_us_config.json).",
    "$(jq -r '.CDR_VERSION_BIGQUERY_DATASET' .all_of_us_config.json)"),
    intern = TRUE)

## BigQuery setup.
BILLING_PROJECT_ID <- Sys.getenv('GOOGLE_PROJECT')
bigrquery::set_service_token(Ronaldo::getServiceAccountKey())

## Plot setup.
theme_set(theme_minimal()) # Default theme for plots.

#' Returns a data frame with a y position and a label, for use annotating ggplot boxplots.
#'
#' @param d A data frame.
#' @return A data frame with column y as max and column label as length.
get_boxplot_fun_data <- function(df) {
  return(data.frame(y = max(df), label = stringr::str_c('N = ', length(df))))
}

## ---------------[ CHANGE THESE AS NEEDED] ---------------------------------------
# Set default parameter values so that all snippets run successfully with no edits needed.
MEASUREMENT_OF_INTEREST <- 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID <- 3000963        # Hemoglobin
UNIT_CONCEPT_ID <- 8713                  # gram per deciliter
MEASUREMENT_NAME <- '<this should be the measurement name>'
UNIT_NAME <- '<this should be the unit name>'
