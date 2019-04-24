"""Auto-generate AoU configuration for Jupyter 'Snippets Menu' extension.

Additionally, create smoke test scripts for both R and Python that include all
the snippets.

See also: https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html
"""

import jinja2
import json
import os

# Output files.
JSON_OUTPUT = 'jupyter_snippets_menu_extension_config.json'
R_SMOKE_TEST = 'smoke_test.R'
PY_SMOKE_TEST = 'smoke_test.py'

# Input file directory.
SNIPPETS_ROOT = '../snippets'

# R configuration constants.
R_SETUP_SNIPPET = 'snippets_setup.R'
R_QUERY_TEMPLATE = '''
{{ dataframe }} <- bq_table_download(bq_project_query(
    BILLING_PROJECT_ID,
    query = str_glue('{{ query }}')))

print(skim({{ dataframe }}))

head({{ dataframe }})
'''

# Python configuration constants.
PY_SETUP_SNIPPET = 'snippets_setup.py'
PY_QUERY_TEMPLATE = """
{{ dataframe }} = pd.io.gbq.read_gbq(f'''
{{ query }}
''',
  project_id=BILLING_PROJECT_ID,
  dialect='standard')

{{ dataframe }}.head()
"""

r_setup_snippet = {
  'name': 'Setup',
  'snippet': open(os.path.join(SNIPPETS_ROOT, R_SETUP_SNIPPET), 'r').read()
}

py_setup_snippet = {
  'name': 'Setup',
  'snippet': open(os.path.join(SNIPPETS_ROOT, PY_SETUP_SNIPPET), 'r').read()
}

r_snippets_config = {
  'name': 'AoU R snippets',
  'sub-menu': [r_setup_snippet]  # The loop below will add more here.
}

py_snippets_config = {
  'name': 'AoU Py snippets',
  'sub-menu': [py_setup_snippet]  # The loop below will add more here.
}

snippets_config = {
  'name': 'AoU snipppets',
  'sub-menu': [r_snippets_config, py_snippets_config]
}

for root, dirs, files in os.walk(SNIPPETS_ROOT):
  # This sort, along with our filenaming convention, ensures that the SQL
  # snippet will occur before the dependent plot snippets.
  files.sort()

  for filename in files:
    # This file may or may not be used for a snippet in a particular language.
    r_code_snippet = None
    py_code_snippet = None

    # Render SQL to snippets in both languages.
    if filename.endswith('.sql'):
      sql = open(os.path.join(SNIPPETS_ROOT, filename), 'r').read()
      r_code_snippet = jinja2.Template(R_QUERY_TEMPLATE).render(
          {'dataframe': filename.replace('.sql', '_df'), 'query': sql})
      py_code_snippet = jinja2.Template(PY_QUERY_TEMPLATE).render(
          {'dataframe': filename.replace('.sql', '_df'), 'query': sql})

    elif filename.endswith('.ggplot'):
      r_code_snippet = open(os.path.join(SNIPPETS_ROOT, filename), 'r').read()

    elif filename.endswith('.plotnine'):
      py_code_snippet = open(os.path.join(SNIPPETS_ROOT, filename), 'r').read()

    if r_code_snippet is not None:
      snippet = {}
      snippet['name'] = filename
      snippet['snippet'] = r_code_snippet
      r_snippets_config['sub-menu'].append(snippet)

    if py_code_snippet is not None:
      snippet = {}
      snippet['name'] = filename
      snippet['snippet'] = py_code_snippet
      py_snippets_config['sub-menu'].append(snippet)

with open(JSON_OUTPUT, 'w') as f:
  json.dump(snippets_config, f)

with open(R_SMOKE_TEST, 'w') as f:
  f.write('#!/usr/bin/env Rscript\n\n')
  for snippet in r_snippets_config['sub-menu']:
    f.write('#---[ This is snippet: {} ]---\n{}\n\n'.format(snippet['name'],
                                                            snippet['snippet']))

with open(PY_SMOKE_TEST, 'w') as f:
  f.write('#!/usr/bin/env python3\n\n')
  for snippet in py_snippets_config['sub-menu']:
    f.write('#---[ This is snippet: {} ]---\n{}\n\n'.format(snippet['name'],
                                                            snippet['snippet']))
