"""Methods to obtains paths to files within the workspace bucket."""

import datetime
import fnmatch
import os
from typing import Dict
from typing import List
from typing import NamedTuple


WorkspaceDestination = NamedTuple('WorkspaceDestination', [('html_file', str), ('comment_file', str)])


class WorkspacePaths:
  """Encapsulate all logic for manipulating workspace paths.

  Paths are of the form:
    gs://fc-secure-<guid>/reports/<user>@researchallofus.org/<date>/<time>/<notebook>.html
    gs://fc-secure-<guid>/reports/<user>@researchallofus.org/<date>/<time>/<notebook>.html.comment.txt

  For example:
    gs://fc-secure-83282461-002f-4bad-86a9-59fdfd11b933/reports/deflaux@researchallofus.org/20200624/211319/Create a version from any of your workspaces.html
    gs://fc-secure-83282461-002f-4bad-86a9-59fdfd11b933/reports/deflaux@researchallofus.org/20200624/211319/Create a version from any of your workspaces.html.comment.txt
  """
  MANAGED_NOTEBOOKS_FOLDER = 'notebooks'
  HTML_COPIES_FOLDER = 'reports'
  COMMENT_FILE_SUFFIX = '.comment.txt'
  HTML_FILE_SUFFIX = '.html'
  NOTEBOOK_FILE_SUFFIX = '.ipynb'
  USER_GLOB = '*researchallofus.org'
  DATE_GLOB = '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
  TIME_GLOB = '[0-9][0-9][0-9][0-9][0-9][0-9]'
  COMMENT_FILE_GLOB = f'*{COMMENT_FILE_SUFFIX}'
  HTML_FILE_GLOB = f'*{HTML_FILE_SUFFIX}'
  NOTEBOOK_FILE_GLOB = f'*{NOTEBOOK_FILE_SUFFIX}'

  def __init__(self, workspace_bucket: str):
    self.workspace_bucket: str = f'gs://{workspace_bucket}'

  def get_subfolder(self) -> str:
    return os.path.join(self.workspace_bucket, self.HTML_COPIES_FOLDER)

  def formulate_destination_paths(self, notebooks: List[str]) -> Dict[str, WorkspaceDestination]:
    """Formulate paths within the workspace bucket where transformations of notebooka can be stored.

    Args:
      notebooks: List of one or more notebook paths.
    Returns:
      A dictionary of notebooks paths to its corresponding WorkspaceDestination tuple.
    """
    user = os.getenv('OWNER_EMAIL')
    timestamp = datetime.datetime.now().strftime('%Y%m%d/%H%M%S')
    destination = os.path.join(self.get_subfolder(), user, timestamp)
    workspace_destinations = {}
    for notebook in notebooks:
      self._check_path_matches_glob(notebook, self.get_notebook_file_glob())
      remote_html = os.path.join(
          destination, os.path.basename(notebook).replace(self.NOTEBOOK_FILE_SUFFIX, self.HTML_FILE_SUFFIX))
      remote_comment = os.path.join(
          destination, os.path.basename(notebook).replace(self.NOTEBOOK_FILE_SUFFIX, self.COMMENT_FILE_SUFFIX))
      workspace_destinations[notebook] = WorkspaceDestination(
          html_file=remote_html,
          comment_file=remote_comment
      )
    return workspace_destinations

  def get_user_glob(self) -> str:
    return os.path.join(self.get_subfolder(), self.USER_GLOB)

  def get_date_glob(self) -> str:
    return os.path.join(self.get_user_glob(), self.DATE_GLOB)

  def get_time_glob(self) -> str:
    return os.path.join(self.get_date_glob(), self.TIME_GLOB)

  def get_comment_file_glob(self) -> str:
    return os.path.join(self.get_time_glob(), self.COMMENT_FILE_GLOB)

  def get_html_file_glob(self) -> str:
    return os.path.join(self.get_time_glob(), self.HTML_FILE_GLOB)

  def get_notebook_file_glob(self) -> str:
    return os.path.join(self.workspace_bucket, self.MANAGED_NOTEBOOKS_FOLDER, self.NOTEBOOK_FILE_GLOB)

  def add_date_glob_to_path(self, path) -> str:
    self._check_path_matches_glob(path, self.get_user_glob())
    return os.path.join(path, self.DATE_GLOB)

  def add_time_glob_to_path(self, path) -> str:
    self._check_path_matches_glob(path, self.get_date_glob())
    return os.path.join(path, self.TIME_GLOB)

  def add_html_glob_to_path(self, path) -> str:
    self._check_path_matches_glob(path, self.get_time_glob())
    return os.path.join(path, '*html')

  @staticmethod
  def _check_path_matches_glob(path: str, glob_to_match: str):
    if not fnmatch.fnmatch(path, glob_to_match):
      raise ValueError(f'"{path}" does not match "{glob_to_match}"')
