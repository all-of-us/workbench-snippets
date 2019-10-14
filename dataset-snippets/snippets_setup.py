!pip3 install --upgrade --user pandas_profiling statsmodels

import os
import numpy as np
import pandas as pd
import pandas_profiling
import plotnine  # NOTE: if you get error "cannot import name 'factorial'" this is due to the
                 # older version of package statsmodels. Restart your kernel.
from plotnine import *  # Provides a ggplot-like interface to matplotlib.

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
