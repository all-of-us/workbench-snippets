"""Methods for creating and viewing HTML snapshots of notebooks.

It is useful to create and retain HTML snapshots of notebooks to track how results within
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
from multiprocess import Pool
import pandas as pd
import tensorflow as tf
from tqdm import tqdm

from terra_widgets.workspace_metadata import WorkspaceMetadata
from terra_widgets.workspace_paths import WorkspacePaths

# Define this in the outer scope so that it lives for the duration of the Jupyter kernel.
TEMP_HTML = tempfile.NamedTemporaryFile(dir=os.getcwd(), prefix='view_an_html_snapshot_', suffix='.html')


def create_html_snapshot(notebook_paths: List[str],
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
    overwrite: Skip the snapshot creation if the file already exists.
  Returns:
    An HTML object for display.
  """
  if not notebook_paths:
    return HTML('''<div class="alert alert-block alert-danger">
    No notebook was selected. To create an HTML snapshot of a notebook, select the desired notebook.</div>''')
  if not comment:
    return HTML('''<div class="alert alert-block alert-danger">
    No comment was specified. Please provide some context in the comment field
    describing why you wish to make an HTML snapshot of the selected notebook(s) at this time.</div>''')

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
      get_ipython().system(f"set -o xtrace ; jupyter nbconvert --to html --ExtractOutputPreprocessor.enabled=False '{temp_notebook}'")
      temp_html = temp_notebook.replace(WorkspacePaths.NOTEBOOK_FILE_SUFFIX, WorkspacePaths.HTML_FILE_SUFFIX)
      get_ipython().system(f"set -o xtrace ; gsutil cp {noclobber} '{temp_html}' '{destinations[notebook_path].html_file}'")
      # Create and transfer the comment file to the workspace bucket.
      temp_comment = temp_notebook.replace(WorkspacePaths.NOTEBOOK_FILE_SUFFIX, WorkspacePaths.COMMENT_FILE_SUFFIX)
      with open(temp_comment, 'w') as f:
        f.write(comment)
      get_ipython().system(f"set -o xtrace ; gsutil cp {noclobber} '{temp_comment}' '{destinations[notebook_path].comment_file}'")
      get_ipython().system(f"set -o xtrace ; gsutil setmeta -h 'Content-Type:text/plain' '{destinations[notebook_path].comment_file}'")

  # Intentionally empty. 'No clobber' does not throw an error, only warns, so returning success might not be correct.
  return HTML('')


def create_html_snapshot_widget(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI for creating html copies."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='<b>Choose the workspace</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  notebook_chooser = widgets.SelectMultiple(
      options=[],  # This will be populated after a workspace is chosen.
      value=[],
      description='<b>Choose one or more notebooks for which to create an HTML snapshot:</b>',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  commenter = widgets.Textarea(
      value='',
      placeholder='Type a comment here about this HTML snapshot of your notebook',
      description='<b>Comment</b>:',
      disabled=False,
      layout=widgets.Layout(width='900px', height='50px'),
      style={'description_width': 'initial'}
  )
  submit_button = widgets.Button(
      description='Submit',
      disabled=False,
      button_style='success',
      tooltip='Click the submit button to create the HTML snapshot.'
  )

  def on_button_clicked(_):
    with output:
      output.clear_output()
      if workspace_chooser.value is None:
        display(HTML('''<div class="alert alert-block alert-danger">
        No workspace was selected. To create an HTML snapshot of a notebook, select the desired workspace.</div>'''))
        return
      workspace_paths = ws_paths[workspace_chooser.value]
      display(create_html_snapshot(notebook_paths=notebook_chooser.value,
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
      [widgets.HTML('''
       <h3>Create an HTML snapshot of a notebook</h3>
       <p>Use this when you want to save an HTML snapshot of a notebook containing its outputs. The notebook will be rendered to HTML as-is (not re-run).
       <br>It will be saved in the <code>reports</code> folder of the workspace bucket:
       <br><ul>
         <li><code>gs://&lt;workspace bucket name&gt;/reports/&lt;your email address&gt;/&lt;date&gt;/&lt;time&gt;/&lt;notebook&gt;.html</code></li>
         <li><code>gs://&lt;workspace bucket name&gt;/reports/&lt;your email address&gt;/&lt;date&gt;/&lt;time&gt;/&lt;notebook&gt;.comment.txt</code></li>
         </ul>
       </p><hr>
       '''),
       workspace_chooser, notebook_chooser, commenter, submit_button],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def create_view_files_widget(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI to view HTML snapshots and their associated comment files."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='<b>Choose the workspace</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  user_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='<b>Choose the user</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  date_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='<b>Choose the date</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  time_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='<b>Choose the time</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  file_chooser = widgets.Dropdown(
      options=[],
      value=None,
      description='<b>Choose the file</b>:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='900px')
  )
  view_comment_button = widgets.Button(
      description='View the comment for the HTML snapshot',
      disabled=False,
      button_style='success',
      layout=widgets.Layout(width='300px'),
      tooltip='Click the button to view the comment associated with the HTML snapshot of the notebook.'
  )
  view_html_button = widgets.Button(
      description='View the HTML snapshot',
      disabled=False,
      button_style='success',
      layout=widgets.Layout(width='250px'),
      tooltip='Click the button to view the HTML snapshot of the notebook.'
  )

  def on_view_comment_button_clicked(_):
    with output:
      output.clear_output()
      if not file_chooser.value:
        display(HTML('''<div class="alert alert-block alert-warning">
        No comment files found for HTML snapshots in this workspace.</div>'''))
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
        No HTML snapshots found in this workspace.</div>'''))
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
      [widgets.HTML('''
       <h3>View an HTML snapshot of a notebook</h3>
       <p>Use the dropdowns to select the workspace, user, date, time, and particular HTML snapshot.
       <br>Then click on the 'view' buttons to see either the comment for the snapshot or the actual snapshot.
       </p><hr>'''),
       workspace_chooser, user_chooser, date_chooser, time_chooser, file_chooser,
       widgets.HBox([view_comment_button, view_html_button])],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def create_view_all_comments_widget(ws_names2id: Dict[str, str], ws_paths: Dict[str, WorkspacePaths], output):
  """Create an ipywidget UI to display the contents of all comment files within a particular workspace."""
  workspace_chooser = widgets.Dropdown(
      options=ws_names2id,
      value=None,
      description='<b>Choose a workspace to view:</b>',
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
          No comment files found for HTML snapshots in this workspace.</div>'''))
        return

      def get_comment(f):
        return get_ipython().getoutput(f"gsutil cat '{f}'")

      def process_task(f):
        return f, get_comment(f)

      max_pool = 16
      with Pool(max_pool) as p:
        pool_outputs = list(tqdm(p.imap(process_task, comment_files), total=len(comment_files)))

      comments = pd.DataFrame.from_dict({f.replace(workspace_paths.get_subfolder(), ''): c[0] for f, c in pool_outputs},
                                        orient = 'index',
                                        columns = ['comment']
                                       ).reset_index()
      comments[['extra', 'author', 'date', 'time', 'item']] = comments['index'].str.split(pat='/', expand=True)
      display(comments[['date', 'time', 'author', 'item', 'comment']].sort_values(by=['date', 'time']))
  workspace_chooser.observe(on_choose_workspace, names='value')

  return widgets.VBox(
      [widgets.HTML('''
       <h3>View all comments for a workspace</h3>
       <p>Use the dropdown to choose a workspace. Then this will display the contents of all comment files for the selected workspace.
       <br>The user, date, time, and notebook name are shown in the left column. The comment is shown in the right column.
       </p><hr>'''),
       workspace_chooser],
      layout=widgets.Layout(width='auto', border='solid 1px grey'))


def display_html_snapshots_widget():
  """Create an ipywidget UI encapsulating all three UIs related to HTML snapshots."""
  if not get_ipython():
    print('The HTML snapshot widget cannot be display in environments other than IPython.')
    return

  # Configure notebook display preferences to better suit this UI. These display settings
  # will be in effect for all cells in the notebook run after this one is run.
  pd.set_option('display.max_colwidth', None)
  pd.set_option('display.max_rows', None)
  get_ipython().run_cell_magic(
      'javascript',
      '',
      '''// Display cell outputs to full height (no vertical scroll bar)
         IPython.OutputArea.auto_scroll_threshold = 9999;''')

  # Retrieve the workspace metadata for the current user and environment.
  ws_meta = WorkspaceMetadata()
  workspace_names2id = collections.OrderedDict(sorted(
      ws_meta.get_workspace_name_to_id_mapping().items()))
  workspace_names2id_include_readonly = collections.OrderedDict(sorted(
      ws_meta.get_workspace_name_to_id_mapping(include_private_readonly=True).items()))
  workspace_ids2bucket_include_readonly = ws_meta.get_workspace_id_to_bucket_mapping(include_private_readonly=True)
  workspace_paths = {k: WorkspacePaths(workspace_bucket=v)
                     for k, v in workspace_ids2bucket_include_readonly.items()}

  ui_output = widgets.Output()

  ui_tabs = widgets.Tab()
  ui_tabs.children = [create_html_snapshot_widget(ws_names2id=workspace_names2id,
                                                  ws_paths=workspace_paths,
                                                  output=ui_output),
                      create_view_files_widget(ws_names2id=workspace_names2id_include_readonly,
                                               ws_paths=workspace_paths,
                                               output=ui_output),
                      create_view_all_comments_widget(ws_names2id=workspace_names2id_include_readonly,
                                                      ws_paths=workspace_paths,
                                                      output=ui_output)]
  ui_tabs.set_title(title='Create', index=0)
  ui_tabs.set_title(title='View one', index=1)
  ui_tabs.set_title(title='View all', index=2)

  display(ui_tabs, ui_output)
