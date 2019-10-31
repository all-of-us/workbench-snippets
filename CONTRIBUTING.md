# Get setup for GitHub

1. If you are new to GitHub, don't start here. Instead, work through a GitHub tutorial such as one of these:
    * https://guides.github.com/activities/hello-world/
    * http://r-pkgs.had.co.nz/git.html.
2. Follow [the instructions](https://github.com/all-of-us/workbench#git-secrets) to install [git-secrets](https://github.com/awslabs/git-secrets). Its a git commit hook that *"Prevents you from committing passwords and other sensitive information to a git repository."*.

# How to contribute a snippet

If you want to add/modify a snippet that uses a dataframe from Dataset Builder as its input, then see [dataset-snippets/README](./dataset-snippets/README.md).

Otherwise, see [snippets/README](./snippets/README.md).

# Auto-generation of Jupyter 'Snippets Menu' configuration.

1. Generate the JSON configuration:
    ```
    git clone https://github.com/all-of-us/workbench-snippets.git
    cd workbench-snippets/build
    python3 ./generate_jupyter_snippets_menu_extension_config.py
    # If you get an error about a missing library, run command 'pip3 install --user Jinja2 pyyaml'
    ```
1. Then copy and paste the contents of the newly created file `r_jupyter_snippets_menu_extension_config.json` or `py_jupyter_snippets_menu_extension_config.json` into form field '*JSON string parsed to define custom menus (only used if the option above is checked)*' in the Snippets Menu extension configuration.

For more detail, see the [Snippets Menu](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html) Jupyter extension documentation.

# Testing

To test individual snippets such as plots, the best thing to do is copy and paste them into a notebook on the workbench.

There are more detailed testing instructions in [dataset-snippets/README](./dataset-snippets/README.md#testing) and [snippets/README](./snippets/README.md#testing).
