library(viridis)    # A nice color scheme for plots.
library(ggthemes)   # Common themes to change the look and feel of plots.
library(scales)     # Graphical scales map data to aesthetics in plots.
library(skimr)      # Better summaries of data.
library(lubridate)  # Date library from the tidyverse.
library(bigrquery)  # BigQuery R client.
library(tidyverse)  # Data wrangling packages.

## CHANGE THESE AS NEEDED - default parameter values for snippets.
DATASET <- 'aou-res-curation-output-prod.R2019Q1R2'
MEASUREMENT_OF_INTEREST <- 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID <- 3000963        # Hemoglobin
UNIT_CONCEPT_ID <- 8713                  # gram per deciliter
MEASUREMENT_NAME <- '<this should be the measurement name>'
UNIT_NAME <- '<this should be the unit name>'

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
