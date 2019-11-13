# Dataset Builder snippets

This snippets in this subdirectory are for workbench users who use Dataset Builder to retrieve their data.

# Get setup for GitHub
The instructions are identical for both the SQL snippets and the Dataset Builder Snippets. See [CONTRIBUTING](../CONTRIBUTING.md#get-setup-for-github) for the details. If you are new to `git`, please see the example commands there. 

# How to contribute a snippet to the Dataset Builder snippets menu group

1. Write your snippet of code in your preferred language, R or Python.
    * Try to make your snippet consistent with other snippets in this collection.
        * For data wrangling, use [dplyr](https://dplyr.tidyverse.org/) for R and [pandas](https://pandas.pydata.org/) for Python.
        * For static plots, use [ggplot2](https://ggplot2.tidyverse.org/) for R and [plotnine](https://plotnine.readthedocs.io/en/stable/) for Python.
    * Choose a good prefix and suffix for your snippet file name.
        * See the names of the other files for examples.
        * The file name helps users decide whether the snippet will be useful to them.
    * Put some comments at the top of your snippet to explain its purpose and any assumptions.
1. After you are happy with your new snippet, port it to the other language or file a GitHub issue asking for help from someone else to do this.
1. If your snippet has any inputs or parameters other than a dataframe created by Dataset Builder, add default values for those parameters to both [`snippets_setup.R`](./snippets_setup.R) and [`snippets_setup.py`](./snippets_setup.py) so that your snippet will work as-is.
1. Update [r_dataset_snippets_menu_config.yml](../build/r_dataset_snippets_menu_config.yml) and [py_dataset_snippets_menu_config.yml](../build/py_dataset_snippets_menu_config.yml) to add your snippet where ever you would like it to be displayed within the menu.
1. Send your pull request!

Don't like these conventions? We can change them! This is just a starting point. Keep in mind we'll need to reflect those changes in the auto-generation script described in the next section.

# Auto-generation of Jupyter 'Snippets Menu' configuration

The instructions are identical for both the SQL snippets and the Dataset Builder Snippets. See [CONTRIBUTING](../CONTRIBUTING.md#auto-generation-of-jupyter-snippets-menu-configuration) for the details.

# Testing

## Snippet tests
To test individual snippets such as plots, the best thing to do is copy and paste them into a notebook on the workbench.

## Integration 'smoke tests'
The script to auto-generate the Jupyter Snippets Menu configuration also emits both `r_dataset_snippets_menu_config_smoke_test.R` and `py_dataset_snippets_menu_config_smoke_test.py`. Those scripts each include, respectively, all the R Dataset Builder snippets and all the Python Dataset Builder snippets. If those scripts are run from the workbench environment and there are no obvious bugs in the snippets, they will run start-to-finish without error and emit _"Smoke test complete!"_ when they have completed successfully. (This won't necessarily catch all bugs, but its a good start.)

The Dataset from Dataset Builder is defined in [r_dataset_snippets_menu_config.smoke_test_setup](./r_dataset_snippets_menu_config.smoke_test_setup) and [py_dataset_snippets_menu_config.smoke_test_setup](./py_dataset_snippets_menu_config.smoke_test_setup), respectively. Update it as needed.

To run the R Dataset Builder snippets smoke tests:
```
%%bash

Rscript r_dataset_snippets_menu_config_smoke_test.R  # There will be output, but there should be no errors.
```

To run the Python Dataset Builder snippets smoke tests:
```
%%bash

# Any notebook '!' commands won't work in this context. Comment them out and run them explicitly first.
perl -i -pe 's/!pip/#!pip/g' py_dataset_snippets_menu_config_smoke_test.py
pip3 install --upgrade --user pandas_profiling statsmodels

python3 py_dataset_snippets_menu_config_smoke_test.py  # There will be output, but there should be no errors.
```

# Deployment
The instructions are identical for both the SQL snippets and the Dataset Builder Snippets. See [CONTRIBUTING](../CONTRIBUTING.md#deployment) for the details.
