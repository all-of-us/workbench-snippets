# Get setup for GitHub

Small typos in code or documentation may be edited directly using the GitHub web interface. Otherwise:

1. If you are new to GitHub, don't start here. Instead, work through a GitHub tutorial such as one of these:
    * https://guides.github.com/activities/hello-world/
    * http://r-pkgs.had.co.nz/git.html.
2. Create a fork of https://github.com/all-of-us/workbench-snippets.
3. Clone your fork.
4. Follow [the instructions](https://github.com/all-of-us/workbench#git-secrets) to install [git-secrets](https://github.com/awslabs/git-secrets). It's a git commit hook that *"Prevents you from committing passwords and other sensitive information to a git repository."*.
5. Work from a feature branch. See the [Appendix](#appendix) for detailed `git` commands.

# How to contribute a snippet

If you want to add/modify a snippet that uses a dataframe from Dataset Builder as its input, then see [dataset-snippets/README](./dataset-snippets/README.md).

Otherwise, see the other snippets collections such as [sql-snippets/README](./sql-snippets/README.md) or [storage-snippets/README](./storage-snippets/README.md).

# Auto-generation of Jupyter 'Snippets Menu' configuration

1. Generate the JSON configuration:
    ```
    git clone https://github.com/all-of-us/workbench-snippets.git
    cd workbench-snippets/build
    python3 ./generate_jupyter_snippets_menu_extension_config.py
    # If you get an error about a missing library, run command 'pip3 install --user Jinja2 pyyaml'
    ```
1. Then copy and paste the contents of the newly created json file (such as `r_sql_snippets_menu_config.json` or `py_sql_snippets_menu_config.json` for the [sql-snippets](./sql-snippets/)) into form field '*JSON string parsed to define custom menus (only used if the option above is checked)*' in the Snippets Menu extension configuration.

For more detail, see the [Snippets Menu](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html) Jupyter extension documentation.

# Testing

To test individual snippets such as plots, the best thing to do is copy and paste them into a notebook on the workbench.

There are more detailed testing instructions README for each of the snippets collections, such as [dataset-snippets/README](./dataset-snippets/README.md#testing) or [sql-snippets/README](./sql-snippets/README.md#testing).

# Deployment

For the updated snippets to be incorporated into the Workbench environment, the workbench team needs to trigger a manual process to pull in snippets updates for deployment.

Once this happens, new snippets contents go live in users' Jupyter servers on a rolling basis over a period of a few weeks.

# Appendix

For the workbench-snippets GitHub repository, we are doing ‘merge and squash’ of pull requests. So that means your fork does not match upstream after your pull request has been merged. The easiest way to manage this is to always work in a feature branch, instead of checking changes into your fork’s master branch.


## How to work on a new feature

(1) Get the latest version of the upstream repo

```
git fetch upstream
```

Note: If you get an error saying that upstream is unknown, run the following remote add command and then re-run the fetch command. You only need to do this once per git clone.

```
git remote add upstream https://github.com/all-of-us/workbench-snippets.git
```

(2) Make sure your master branch is “even” with upstream.

```
git checkout master
git merge --ff-only upstream/master
git push
```

Now the master branch of your fork on GitHub should say *"This branch is even with all-of-us:master."*.


(3) Create a feature branch for your change.

```
git checkout -b my-feature-branch-name
```

Because you created this feature branch from your master branch that was up to date with upstream (step 2), your feature branch is also up to date with upstream. Commit your changes to this branch until you are happy with them.

(4) Push your changes to GitHub and send a pull request.

```
git push --set-upstream origin my-feature-branch-name
```

After your pull request is merged, its safe to delete your branch!

## I accidentally checked a new change to my master branch instead of a feature branch. How to fix this?

(1) Soft undo your change(s). This leaves the changes in the files on disk but undoes the commit.

```
git checkout master
# Moves pointer back to previous HEAD
git reset --soft HEAD@{1}
```

Or if you need to move back several commits to the most recent one in common with upstream, you can change ‘1’ to be however many commits back you need to go.

(2) “stash” your now-unchecked-in changes so that you can get them back later.

```
git stash
```

(3) Now do the [How to work on a new feature](#how-to-work-on-a-new-feature) step to bring master up to date and create your new feature branch that is “even” with upstream. Here are those commands again:

```
git fetch upstream
git merge --ff-only upstream/master
git checkout -b my-feature-branch-name
```

(4) “unstash” your changes.

```
git stash pop
```
Now you can proceed with your work!
