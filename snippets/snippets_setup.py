import os
import numpy as np
import pandas as pd
import plotnine
from plotnine import *  # Provides a ggplot-like interface to matplotlib.

## CHANGE THESE AS NEEDED - default parameter values for snippets.
DATASET = 'aou-res-curation-output-prod.R2019Q1R2'
MEASUREMENT_OF_INTEREST = 'hemoglobin'
# Tip: the next four parameters could be set programmatically using one row from
# the result of measurements_of_interest_summary.sql
MEASUREMENT_CONCEPT_ID = 3000963        # Hemoglobin
UNIT_CONCEPT_ID = 8713                  # gram per deciliter
MEASUREMENT_NAME = '<this should be the measurement name>'
UNIT_NAME = '<this should be the unit name>'

## BigQuery setup.
BILLING_PROJECT_ID = os.environ['GOOGLE_PROJECT']

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
