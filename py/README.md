# Terra widgets

A python package for ipywidget-based user interfaces for performing tasks within the context Python Jupyter notebooks running in either the Terra or All of Us workbench environments.


## Create and view HTML snapshots of notebooks

The workbench takes care of saving the current version of your notebooks for you. But what if you want to know **what your notebook looked like two weeks ago?** Use `display_html_snapshots_widget()` to display a widget which can save snapshots of a notebook for later review, allowing users to track changes to results in notebooks over time. To do this, it:

1. Converts the selected notebook to an HTML file (without re-running the notebook).
1. And then copies that HTML file to subfolder within the same workspace bucket where the notebook file is stored.

Use this interface to create an HTML snapshot each time you make a major change to your notebook. You can choose notebooks from **any of your workspaces!**

Implementation details:

* The user interface controls are implemented using the [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/) Python package.

* Notebooks are converted from `.ipynb` to `.html` using [nbconvert](https://nbconvert.readthedocs.io/en/latest/).

* Files are transfered back and forth from the workspace bucket using both:
    * [gsutil](https://cloud.google.com/storage/docs/gsutil)
    * [Tensorflow GFile](https://www.tensorflow.org/api_docs/python/tf/io/gfile/GFile).
    
* The few files of code implementing this interface are preinstalled as a [Python library](https://github.com/all-of-us/workbench-snippets/blob/main/py/setup.py) on the AoU workbench.
