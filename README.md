# Get setup for GitHub

1. If you are new to GitHub, don't start here. Instead, work through a GitHub tutorial such as one of these:
    * https://guides.github.com/activities/hello-world/
    * http://r-pkgs.had.co.nz/git.html.
2. Follow [the instructions](https://github.com/all-of-us/workbench#git-secrets) to install [git-secrets](https://github.com/awslabs/git-secrets). Its a git commit hook that "Prevents you from committing passwords and other sensitive information to a git repository.".

# How to contribute a snippet

1. Write the SQL to retrieve the data of interest.
    * Try to put as much of the data wrangling logic into SQL as possible. This means there's less data wrangling code to write twice (e.g., once in [pandas](https://pandas.pydata.org/) for Python and again [dplyr](https://dplyr.tidyverse.org/) for R).
    * Choose a good prefix for your `<my-query>.sql` file name. The file name helps users decide whether its useful to them. It will also become the name of the dataframe holding the query results (e.g. `<my-query>_df`).
    * Put some comments in your query too. Look at the other `.sql` files for examples.
    * Tip: Paste your SQL into the [BigQuery web UI](https://bigquery.cloud.google.com/) and click on the 'format' button to format it nicely.
1. If your query has any parameter(s) other than `DATASET`, add default values for those parameters to both [`snippets_setup.R`](./snippets/snippets_setup.R) and [`snippets_setup.py`](./snippets/snippets_setup.py) so that the query will work as-is.
1. [Optional] If your SQL is complex, consider writing a test case for it. Look at the other SQL tests for examples.
1. If you want to include any visualizations for the data returned by your query, write a plot that assumes the existence of `<my-query>_df`.
    * Write it first in [ggplot2](https://ggplot2.tidyverse.org/) or [plotnine](https://plotnine.readthedocs.io/en/stable/), depending on your preference, and iterate until you like the look of it.
    * Once you have it the way you want it, port it to the other language.
    * Name the files `<my-query>_<viz-description>.ggplot` and `<my-query>_<viz-description>.plotnine`

Don't like these conventions? We can change them! This is just a starting point. Keep in mind we'll need to reflect those changes in the auto-generation script described in the next section.

# Auto-generation of Jupyter 'Snippets Menu' configuration.

For more detail, see the [Snippets Menu](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html) Jupyter extension documentation.

1. Generate the JSON configuration:
    ```
    git clone https://github.com/all-of-us/code-snippets.git
    cd code-snippets/build
    python3 ./generate_jupyter_snippets_menu_extension_config.py
    # If you get an error about a missing jinja2 library, run command 'pip3 install --user jinja2'
    ```
1. Then copy and paste the contents of the newly created file `jupyter_snippets_menu_extension_config.json` to form field '*JSON string parsed to define custom menus (only used if the option above is checked)*' in the Snippets Menu extension configuration.

# Testing

## Snippet tests
To test individual snippets such as plots, the best thing to do is copy and paste them into a notebook on the workbench.

## Query tests

The logic in some SQL queries can be quite complex, and therefore meriting some test cases. Be sure to represent realistic messiness of the data in the fake data created for each test case. The test framework we use is [BQTestCase](https://github.com/verilylifesciences/analysis-py-utils).

To run a test:
```
# BQTestCase is only compatible with Python 2.7 right now.
pip2.7 install git+https://github.com/verilylifesciences/analysis-py-utils.git@v0.3.0

git clone https://github.com/all-of-us/code-snippets.git
cd code-snippets/build

# This should be the id of a Cloud Platform project to which you can write temporary BigQuery tables.
export TEST_PROJECT=<your-project-id>
python2.7 most_recent_measurement_of_interest_test.py
```

## Integration 'smoke tests'
The script to auto-generate the Jupyter Snippets Menu configuration also emits both `smoke_test.R` and `smoke_test.py`. Those scripts each include, respectively, all the R snippets and all the Python snippets. If those scripts are run from the workbench environment and there are no obvious bugs in the snippets, they will run start-to-finish without error. (It won't necessarily catch all bugs, but its a good start.)

To run the smoke tests:
```
# Check the R snippets.
Rscript smoke_test.R  # There will be output, but there should be no errors.

# Check the Python snippets.
python3 smoke_test.py # There will be output, but there should be no errors.
```
