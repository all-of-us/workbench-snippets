import json
import os
import numpy as np
import pandas as pd
import plotnine
from plotnine import *  # Provides a ggplot-like interface to matplotlib.

## CHANGE THESE AS NEEDED - default parameter values for snippets.
MEASUREMENT_OF_INTEREST = 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID = 3000963        # Hemoglobin
UNIT_CONCEPT_ID = 8713                  # gram per deciliter
MEASUREMENT_NAME = '<this should be the measurement name>'
UNIT_NAME = '<this should be the unit name>'

# Get the BigQuery curated dataset for the current workspace context.
with open('.all_of_us_config.json') as f:
  config = json.load(f)
  DATASET = config['CDR_VERSION_CLOUD_PROJECT'] + '.' + config['CDR_VERSION_BIGQUERY_DATASET']

## Plot setup.
theme_set(theme_minimal()) # Default theme for plots.

def get_boxplot_fun_data(df):
  """Returns a data frame with a y position and a label, for use annotating ggplot boxplots.

  Args:
    d: A data frame.
  Returns:
    A data frame with column y as max and column label as length.
  """
  d = {'y': max(df), 'label': f'N = {len(df)}'}
  return(pd.DataFrame(data=d, index=[0]))
