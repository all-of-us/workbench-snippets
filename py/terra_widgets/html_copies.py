"""Methods for creating and viewing HTML copies of notebooks.

It is useful to create and retain HTML copies of notebooks to track how results within
a notebook changes over time as analysis work proceeds.
"""

import collections
import os
import tempfile
from typing import Dict
from typing import List

from IPython import get_ipython
from IPython.display import display
from IPython.display import HTML
from IPython.display import IFrame
from ipywidgets import widgets
import pandas as pd
import tensorflow as tf

from terra_widgets.workspace_metadata import WorkspaceMetadata
from terra_widgets.workspace_paths import WorkspacePaths

# Define this in the outer scope so that it lives for the duration of the Jupyter kernel.
TEMP_HTML = tempfile.NamedTemporaryFile(dir=os.getcwd(), prefix='view_an_html_copy_', suffix='.html')

# Retrieve the workspace metadata for the current user and environment.
ws_meta = WorkspaceMetadata()
WORKSPACE_NAMES2ID = collections.OrderedDict(sorted(
    ws_meta.get_workspace_name_to_id_mapping().items()))
WORKSPACE_NAMES2ID_INCLUDE_READONLY = collections.OrderedDict(sorted(
    ws_meta.get_workspace_name_to_id_mapping(include_private_readonly=True).items()))
WORKSPACE_IDS2BUCKET_INCLUDE_READONLY = ws_meta.get_workspace_id_to_bucket_mapping(include_private_readonly=True)
WORKSPACE_PATHS = {k: WorkspacePaths(workspace_bucket=v)
                   for k, v in WORKSPACE_IDS2BUCKET_INCLUDE_READONLY.items()}

# Configure notebook display preferences to better suit this UI.
if pd.__version__.startswith('1'):
  pd.set_option('display.max_colwidth', None)
else:
  pd.set_option('display.max_colwidth', -1)
get_ipython().run_cell_magic(
    'javascript',
    '',
    '''// Display cell outputs to full height (no vertical scroll bar)
       IPython.OutputArea.auto_scroll_threshold = 9999;''')


def create_html_copy(notebook_paths: List[str],
                     comment: str,
                     workspace_paths: WorkspacePaths,
                     overwrite: bool = False) -> HTML:
  """Render a notebook to HTML and transfer the HTML and its comment to the workspace bucket.

  The notebook is rendered as-is (it is not re-run). The comment is stored in a file in the same folder as the HTML.

  Note, there's a mix of TensorFlow GFile in here and gsutil. We use GFile while the file could be
  either local or remote. We use gsutil when its definitely remote because the console output serves as
  useful progress messages.

  Args:
    notebook_paths: A list of Cloud Storage paths to the notebooks for which to create HTML
    comment: A string to be associated with the HTML file(s) such as a description of recent
             changes to the notebook and the results within it.
    workspace_paths: A list of WorkspacePaths objects indicating the destinations for the HTML and comment files.
    overwrite: Skip the copy creation if the file already exists.
  Returns:
    An HTML object for display.
  """
  if not notebook_paths:
    return HTML('''<div class="alert alert-block alert-danger">
    No notebook was selected. To create an HTML copy of a notebook, select the desired notebook.</div>''')
  if not comment:
    return HTML('''<div class="alert alert-block alert-danger">
    No comment was specified. Please provide some context in the comment field
    describing why you wish to make an HTML copy of the selected notebook(s) at this time.</div>''')

  destinations = workspace_paths.formulate_destination_paths(notebooks=notebook_paths)

  with tempfile.TemporaryDirectory() as tmpdirname:
    for notebook_path in notebook_paths:
      temp_notebook = os.path.join(tmpdirname, os.path.basename(notebook_path))
      try:
        tf.io.gfile.copy(src=notebook_path, dst=temp_notebook)
      except (tf.errors.NotFoundError, tf.errors.PermissionDeniedError) as e:
        return HTML(f'''<div class="alert alert-block alert-danger">
        <b>Warning:</b> Unable to copy {notebook_path} to {temp_notebook}.
        <hr><p><pre>{e.message}</pre></p></div>''')

      noclobber = '-n' if not overwrite else ''
      # Create and transfer the html file to the workspace bucket.
      get_ipython().system(f"set -o xtrace ; jupyter nbconvert --to html_toc --ExtractOutputPreprocessor.enabled=False '{temp_notebook}'")
      temp_html = temp_notebook.replace('.ipynb', '.html')
      get_ipython().system(f"set -o xtrace ; gsutil cp {noclobber} '{temp_html}' '{destinations[notebook_path].html_file}'")
      # Create and transfer the comment file to the workspace bucket.
      get_ipython().system(f"set -o xtrace ; echo '{comment}' | gsutil cp {noclobber} - '{destinations[notebook_path].comment_file}'")
      get_ipython().system(f"set -o xtrace ; gsutil setmeta -h 'Content-Type:text/plain' '{destinations[notebook_path].comment_file}'")

  # Intentionally empty. 'No clobber' does not throw an error, only warns, so returning success might not be correct.
  return HTML('')


def create_html_copy_ui(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI for creating html copies."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='Choose the workspace:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  notebook_chooser = widgets.SelectMultiple(
      options=[],  # This will be populated after a workspace is chosen.
      value=[],
      description='Choose one or more notebooks for which to create an HTML copy:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  commenter = widgets.Textarea(
      value='',
      placeholder='Type a comment here about this HTML copy of your notebook',
      description='Comment:',
      disabled=False,
      layout=widgets.Layout(width='900px', height='50px'),
      style={'description_width': 'initial'}
  )
  submit_button = widgets.Button(
      description='Submit',
      disabled=False,
      button_style='success',
      tooltip='Click the submit button to create the HTML copy'
  )

  def on_button_clicked(_):
    with output:
      output.clear_output()
      if workspace_chooser.value is None:
        display(HTML('''<div class="alert alert-block alert-danger">
        No workspace was selected. To create an HTML copy of a notebook, select the desired workspace.</div>'''))
        return
      workspace_paths = ws_paths[workspace_chooser.value]
      display(create_html_copy(notebook_paths=notebook_chooser.value,
                               comment=commenter.value,
                               workspace_paths=workspace_paths))
  submit_button.on_click(on_button_clicked)

  def on_choose_workspace(changed):
    output.clear_output()
    workspace_paths = ws_paths[changed['new']]
    workspace_notebooks = tf.io.gfile.glob(pattern=workspace_paths.get_notebook_file_glob())
    notebook_chooser.options = {os.path.basename(nb): nb for nb in workspace_notebooks}
  workspace_chooser.observe(on_choose_workspace, names='value')

  return widgets.VBox(
      [widgets.HTML('<h3>Create an HTML copy of a notebook</h3>'), workspace_chooser, notebook_chooser,
       commenter, submit_button],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def view_files_ui(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI to view HTML copies and their associated comment files."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='Choose the workspace:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  user_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='Choose the user:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  date_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='Choose the date:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  time_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='Choose the time:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  file_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='Choose the file:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  view_html_button = widgets.Button(
      description='View the HTML copy',
      disabled=False,
      button_style='success',
      layout=widgets.Layout(width='250px'),
      tooltip='Click the button to view the HTML copy of the notebook.'
  )
  view_comment_button = widgets.Button(
      description='View the comment for the HTML copy',
      disabled=False,
      button_style='success',
      layout=widgets.Layout(width='250px'),
      tooltip='Click the button to view the comment associated with the HTML copy of the notebook.'
  )

  def on_view_comment_button_clicked(_):
    with output:
      output.clear_output()
      if not file_chooser.value:
        display(HTML('''<div class="alert alert-block alert-warning">
        No comment files found for HTML copies in this workspace.</div>'''))
        return
      comment_file = file_chooser.value.replace('.html', WorkspacePaths.COMMENT_FILE_SUFFIX)
      comment = get_ipython().getoutput(f"gsutil cat '{comment_file}'")
      display(HTML(f'''<div class="alert alert-block alert-info">{comment}</div>'''))
  view_comment_button.on_click(on_view_comment_button_clicked)

  def on_view_html_button_clicked(_):
    with output:
      output.clear_output()
      if not file_chooser.value:
        display(HTML('''<div class="alert alert-block alert-warning">
        No HTML copies found in this workspace.</div>'''))
        return
      source = file_chooser.value
      dest = TEMP_HTML.name
      get_ipython().system(f"set -o xtrace ; gsutil cp '{source}' '{dest}'")
      display(IFrame(os.path.join('.', os.path.basename(TEMP_HTML.name)), width='100%', height=800))
  view_html_button.on_click(on_view_html_button_clicked)

  def on_choose_workspace(changed):
    output.clear_output()
    user_chooser.options = []
    if changed['new']:
      workspace_paths = ws_paths[changed['new']]
      items = tf.io.gfile.glob(pattern=workspace_paths.get_user_glob())
      if items:
        user_chooser.options = {os.path.basename(item): item for item in items}
  workspace_chooser.observe(on_choose_workspace, names='value')

  def on_choose_user(changed):
    date_chooser.options = []
    if changed['new']:
      workspace_paths = ws_paths[workspace_chooser.value]
      items = tf.io.gfile.glob(pattern=workspace_paths.add_date_glob_to_path(path=changed['new']))
      if items:
        date_chooser.options = collections.OrderedDict(sorted(
            {os.path.basename(item): item for item in items}.items(), reverse=True))
  user_chooser.observe(on_choose_user, names='value')

  def on_choose_date(changed):
    time_chooser.options = []
    if changed['new']:
      workspace_paths = ws_paths[workspace_chooser.value]
      items = tf.io.gfile.glob(pattern=workspace_paths.add_time_glob_to_path(path=changed['new']))
      if items:
        time_chooser.options = collections.OrderedDict(sorted(
            {os.path.basename(item): item for item in items}.items(), reverse=True))
  date_chooser.observe(on_choose_date, names='value')

  def on_choose_time(changed):
    file_chooser.options = []
    if changed['new']:
      workspace_paths = ws_paths[workspace_chooser.value]
      items = tf.io.gfile.glob(pattern=workspace_paths.add_html_glob_to_path(path=changed['new']))
      if items:
        file_chooser.options = {os.path.basename(item): item for item in items}
  time_chooser.observe(on_choose_time, names='value')

  return widgets.VBox(
      [widgets.HTML('<h3>View an HTML copy of a notebook</h3>'), workspace_chooser, user_chooser,
       date_chooser, time_chooser, file_chooser, widgets.HBox([view_comment_button, view_html_button])],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def view_all_comments_ui(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI to display the contents of all comment files within a particular workspace."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='Choose a workspace to view:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )

  def on_choose_workspace(changed):
    with output:
      output.clear_output()
      workspace_paths = ws_paths[changed['new']]
      comment_files = get_ipython().getoutput(f'gsutil ls {workspace_paths.get_comment_file_glob()}')
      if not comment_files[0].startswith('gs://'):
        display(HTML('''<div class="alert alert-block alert-warning">
          No comment files found for HTML copies in this workspace.</div>'''))
        return
      progress = widgets.IntProgress(
          value=0,
          min=0,
          max=len(comment_files),
          step=1,
          description=f'Retrieving {len(comment_files)} comments:',
          bar_style='success',
          orientation='horizontal',
          layout=widgets.Layout(width='450px'),
          style={'description_width': 'initial'}
      )
      display(progress)
      comment_num = 0
      comment_file_contents = []
      for file in comment_files:
        comment = get_ipython().getoutput(f"gsutil cat '{file}'")
        version = file.replace(workspace_paths.get_subfolder(), '')
        comment_file_contents.append({'version': version, 'comment': comment})
        comment_num += 1
        progress.value = comment_num
      comments = pd.DataFrame(comment_file_contents)
      display(comments)
  workspace_chooser.observe(on_choose_workspace, names='value')

  return widgets.VBox(
      [widgets.HTML('<h3>View all comments for a workspace</h3>'), workspace_chooser],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def html_copies_ui():
  """Create an ipywidget UI encapsulating all three UIs related to HTML copies."""
  ui_output = widgets.Output()

  ui_tabs = widgets.Tab()
  ui_tabs.children = [create_html_copy_ui(ws_names2id=WORKSPACE_NAMES2ID,
                                          ws_paths=WORKSPACE_PATHS,
                                          output=ui_output),
                      view_files_ui(ws_names2id=WORKSPACE_NAMES2ID_INCLUDE_READONLY,
                                    ws_paths=WORKSPACE_PATHS,
                                    output=ui_output),
                      view_all_comments_ui(ws_names2id=WORKSPACE_NAMES2ID_INCLUDE_READONLY,
                                           ws_paths=WORKSPACE_PATHS,
                                           output=ui_output)]
  ui_tabs.set_title(title='Create', index=0)
  ui_tabs.set_title(title='View one', index=1)
  ui_tabs.set_title(title='View all', index=2)

  display(ui_tabs, ui_output)
