"""Methods to obtain workspace metadata for the current user in various formats."""

import json
import os
from typing import Dict

import firecloud.api as fapi
from IPython import get_ipython

AOU_DOMAIN = '@researchallofus.org'
EDIT_ACCESS_LEVELS = ['WRITER', 'OWNER', 'PROJECT_OWNER']


class WorkspaceMetadata:
  """Encapsulate all logic for obtaining workspace metadata."""

  def __init__(self):
    self.user = os.getenv('OWNER_EMAIL')
    self.terra_workspaces = fapi.list_workspaces().json()
    if self.user.endswith(AOU_DOMAIN):
      # Use the All of Us API to get the human-readable workspace names. For All of Us workspaces,
      # the Terra workspace metadata the workspace names are actually the AoU workspace ids.
      aou_response = get_ipython().getoutput('''curl -H "Content-Type: application/json" \
          -H "Authorization: Bearer $(gcloud auth print-access-token)" \
          "https://api.workbench.researchallofus.org/v1/workspaces" 2>/dev/null | jq .''')
      self.aou_workspaces = json.loads(''.join(aou_response))['items']
    else:
      self.aou_workspaces = None

  def get_workspace_name_to_id_mapping(self, include_private_readonly: bool = False, include_all: bool = False) -> Dict[str, str]:
    """Retrieve a mapping of workspace names to ids.

    Args:
      include_private_readonly: whether to include private workspaces for which the current user has only has read access.
      include_all: whether to include all workspaces visible to the user
    Returns:
      A dictionary of workspace names to workspace ids.
    """
    if self.aou_workspaces:
      return {ws['workspace']['name']: ws['workspace']['id'] for ws in self.aou_workspaces
              if include_all
              or (include_private_readonly and not ws['workspace']['published'])
              or ws['accessLevel'] in EDIT_ACCESS_LEVELS}
    else:
      return {ws['workspace']['name']: ws['workspace']['workspaceId'] for ws in self.terra_workspaces
              if include_all
              or (include_private_readonly and not ws['public'])
              or ws['accessLevel'] in EDIT_ACCESS_LEVELS}

  def get_workspace_name_to_bucket_mapping(self, include_private_readonly: bool = False, include_all: bool = False) -> Dict[str, str]:
    """Retrieve a mapping of workspace names to Cloud Storage bucket names.

    Args:
      include_private_readonly: whether to include private workspaces for which the current user has only has read access.
      include_all: whether to include all workspaces visible to the user
    Returns:
      A dictionary of workspace names to workspace bucket names.
    """
    ws_mapping = self.get_workspace_name_to_id_mapping(include_private_readonly=include_private_readonly,
                                                       include_all=include_all)
    if self.aou_workspaces:
      # For All of Us workspaces, in the Terra workspace metadata the workspace names are actually
      # the AoU workspace ids.
      terra_ws_names = ws_mapping.values()
    else:
      terra_ws_names = ws_mapping.keys()
    return {ws['workspace']['name']: ws['workspace']['bucketName'] for ws in self.terra_workspaces
            if ws['workspace']['name'] in terra_ws_names}

  def get_workspace_id_to_bucket_mapping(self, include_private_readonly: bool = False, include_all: bool = False) -> Dict[str, str]:
    """Retrieve a mapping of workspace ids to Cloud Storage bucket names.

    Args:
      include_private_readonly: whether to include private workspaces for which the current user has only has read access.
      include_all: whether to include all workspaces visible to the user
    Returns:
      A dictionary of workspace names to workspace bucket names.
    """
    ws_mapping = self.get_workspace_name_to_id_mapping(include_private_readonly=include_private_readonly,
                                                       include_all=include_all)
    if self.aou_workspaces:
      # For All of Us workspaces, in the Terra workspace metadata the workspace names are actually
      # the AoU workspace ids.
      terra_metadata_key = 'name'
    else:
      terra_metadata_key = 'workspaceId'
    return {ws['workspace'][terra_metadata_key]: ws['workspace']['bucketName'] for ws in self.terra_workspaces
            if ws['workspace'][terra_metadata_key] in ws_mapping.values()}
