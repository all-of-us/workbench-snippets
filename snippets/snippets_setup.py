!pip3 install --upgrade --user statsmodels

import json
import os
import numpy as np
import pandas as pd
import plotnine
from plotnine import *  # Provides a ggplot-like interface to matplotlib.

# Get the BigQuery curated dataset for the current workspace context.
CDR = os.environ['WORKSPACE_CDR']

## Plot setup.
theme_set(theme_bw(base_size = 11)) # Default theme for plots.

def get_boxplot_fun_data(df):
  """Returns a data frame with a y position and a label, for use annotating ggplot boxplots.

  Args:
    d: A data frame.
  Returns:
    A data frame with column y as max and column label as length.
  """
  d = {'y': max(df), 'label': f'N = {len(df)}'}
  return(pd.DataFrame(data=d, index=[0]))

## ---------------[ CHANGE THESE AS NEEDED] ---------------------------------------
# Set default parameter values so that all snippets run successfully with no edits needed.
COHORT_QUERY = f'SELECT person_id FROM `{CDR}.person`'  # Default to all participants.
MEASUREMENT_OF_INTEREST = 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID = 3000963        # Hemoglobin
UNIT_CONCEPT_ID = 8636                  # gram per liter
MEASUREMENT_NAME = '<this should be the measurement name>'
UNIT_NAME = '<this should be the unit name>'

# NOTE: if you get any errors from this cell, restart your kernel and run it again.
