# SQL snippets

This snippets in this subdirectory are for workbench users who either know SQL or want to learn how to use SQL.

# Get setup for GitHub
The instructions are identical for all of the snippets collections. See [CONTRIBUTING](../CONTRIBUTING.md#get-setup-for-github) for the details. If you are new to `git`, please see the example commands there. 

# How to contribute a snippet to the SQL snippets menu group

1. Write the SQL to retrieve the data of interest.
    * Try to put as much of the data wrangling logic into SQL as possible. This means there's less data wrangling code to write twice (e.g., once in [pandas](https://pandas.pydata.org/) for Python and again [dplyr](https://dplyr.tidyverse.org/) for R).
    * Choose a good prefix for your `<my-query>.sql` file name. The file name helps users decide whether its useful to them. It will also become the name of the dataframe holding the query results (e.g. `<my-query>_df`).
    * Put some comments in your query too. Look at the other `.sql` files for examples.
    * Tip: Paste your SQL into the [BigQuery web UI](https://bigquery.cloud.google.com/) and click on the 'format' button to format it nicely.
1. If your query has any parameter(s) other than `DATASET`, add default values for those parameters to both [`snippets_setup.R`](./snippets_setup.R) and [`snippets_setup.py`](./snippets_setup.py) so that the query will work as-is.
1. [Optional] If your SQL is complex, consider writing a test case for it. Look at the other SQL tests for examples.
1. If you want to include any visualizations for the data returned by your query, write a plot that assumes the existence of `<my-query>_df`.
    * Write it first in [ggplot2](https://ggplot2.tidyverse.org/) or [plotnine](https://plotnine.readthedocs.io/en/stable/), depending on your preference, and iterate until you like the look of it.
    * Once you have it the way you want it, port it to the other language.
    * Name the files `<my-query>_<viz-description>.ggplot` and `<my-query>_<viz-description>.plotnine`
1. Update [r_sql_snippets_menu_config.yml](../build/r_sql_snippets_menu_config.yml) and [py_sql_snippets_menu_config.yml](../build/py_sql_snippets_menu_config.yml) to add your snippet where ever you would like it to be displayed within the menu.
1. Send your pull request!

Don't like these conventions? We can change them! This is just a starting point. Keep in mind we'll need to reflect those changes in the auto-generation script described in the next section.

# Auto-generation of Jupyter 'Snippets Menu' configuration

The instructions are identical for all of the snippets collections. See [CONTRIBUTING](../CONTRIBUTING.md#auto-generation-of-jupyter-snippets-menu-configuration) for the details.

# Testing

## Snippet tests
To test individual snippets such as plots, the best thing to do is copy and paste them into a notebook on the workbench.

## Query tests

The logic in some SQL queries can be quite complex, and therefore meriting some test cases. Be sure to represent realistic messiness of the data in the fake data created for each test case. The test framework we use is [BQTestCase](https://github.com/verilylifesciences/analysis-py-utils).

To run a test:
```
# BQTestCase is only compatible with Python 2.7 right now.
pip2.7 install git+https://github.com/verilylifesciences/analysis-py-utils.git@v0.3.0

git clone https://github.com/all-of-us/workbench-snippets.git
cd workbench-snippets/sql-snippets

# This should be the id of a Cloud Platform project to which you can write temporary BigQuery tables.
export TEST_PROJECT=<your-project-id>
python2.7 most_recent_measurement_of_interest_test.py
```

We cannot current run these tests from the workbench because we are unable to create the BigQuery tables with syntheic data. Instead, run them from an environment such as [Terra](https://app.terra.bio/) or [Cloud Shell](https://cloud.google.com/shell/).

## Integration 'smoke tests'
If the smoke tests are run from the workbench environment and there are no obvious bugs in the snippets, they will run start-to-finish without error. (This won't necessarily catch all bugs, but its a good start.)

* The script to auto-generate the Jupyter Snippets Menu configuration also emits both `r_sql_snippets_menu_config_smoke_test.R` and `py_sql_snippets_menu_config_smoke_test.py`.
* Those scripts each include, respectively, all the R SQL snippets and all the Python SQL snippets.
* The CDR that will be used is determined by the `WORKBENCH_CDR` environment variable. The example below shows how to override it, if desired.

After opening a notebook in the production workbench environment, upload these smoke test files into Jupyter and then execute the following code from the Jupyter terminal or a Python notebook in the same directory. They will emit _"Smoke test complete!"_ when they have completed successfully.

To run the R SQL snippets smoke tests:
```
%%bash

export WORKSPACE_CDR='fc-aou-cdr-prod.THE-CDR-YOU-WANT-TO-TEST-AGAINST'
Rscript r_sql_snippets_menu_config_smoke_test.R  # There will be output, but there should be no errors.
```

To run the Python SQL snippets smoke tests:
```
%%bash

export WORKSPACE_CDR='fc-aou-cdr-prod.THE-CDR-YOU-WANT-TO-TEST-AGAINST'

python3 py_sql_snippets_menu_config_smoke_test.py  # There will be output, but there should be no errors.
```

# Deployment
The instructions are identical for all of the snippets collections. See [CONTRIBUTING](../CONTRIBUTING.md#deployment) for the details.
