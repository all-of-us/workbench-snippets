"""Auto-generate All of Us configuration for Jupyter 'Snippets Menu' extension.

Additionally, create smoke test scripts for both R and Python that include all
the snippets.

See also: https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html
"""

import jinja2
import json
import os
import yaml

# Input file directory.
SNIPPETS_ROOT = '../'

R_MENU_CONFIG = './r_snippets_menu_config.yml'
PY_MENU_CONFIG = './py_snippets_menu_config.yml'

R_QUERY_TEMPLATE = '''
{{ dataframe }} <- bq_table_download(bq_project_query(
    BILLING_PROJECT_ID,
    query = str_glue('{{ query }}')))

print(skim({{ dataframe }}))

head({{ dataframe }})
'''

PY_QUERY_TEMPLATE = """
{{ dataframe }} = pd.io.gbq.read_gbq(f'''
{{ query }}
''',
  dialect='standard')

{{ dataframe }}.head()
"""

R_SHEBANG = '#!/usr/bin/env Rscript\n\n'
PY_SHEBANG = '#!/usr/bin/env python3\n\n'

# Output files.
R_JSON_OUTPUT = 'r_jupyter_snippets_menu_extension_config.json'
PY_JSON_OUTPUT = 'py_jupyter_snippets_menu_extension_config.json'
R_SMOKE_TEST = 'smoke_test.R'
PY_SMOKE_TEST = 'smoke_test.py'


def generate_config(d, query_template, smoke_test_fh):
  """Given a dictionary, convert that to snippets menu configuration."""
  for key, value in d.items():
    if isinstance(value, list):
      return {
          'name': key,
          'sub-menu': [generate_config(x, query_template, smoke_test_fh)
                       for x in value]
      }

    if value == 'divider':
      return '---'

    if value.startswith('http'):
      return {
          'name': key,
          'external-link': value
      }

    if os.path.isfile(os.path.join(SNIPPETS_ROOT, value)):
      if value.endswith('.sql'):
        # Render SQL to snippets in the desired language.
        sql = open(os.path.join(SNIPPETS_ROOT, value), 'r').read()
        dataframe_name = os.path.splitext(os.path.basename(value))[0] + '_df'
        code = jinja2.Template(query_template).render(
            {'dataframe': dataframe_name, 'query': sql})
      else:
        # Its a non-sql file, just read it in.
        code = open(os.path.join(SNIPPETS_ROOT, value), 'r').read()

      smoke_test_fh.write('#---[ This is snippet: {} ]---\n{}\n\n'.format(key,
                                                                          code))
      return {
          'name': key,
          'snippet': code
      }

    # Its not a file, so we will use the value directly.
    return {
        'name': key,
        'snippet': value
    }


def render_files(config_file, query_template, output_file,
                 shebang, smoke_test_file):
  """Use configuration to drive the autogeneration of snippets and tests."""
  with open(config_file, 'r') as f:
    config = yaml.load(f.read())

  print(yaml.dump(config))

  with open(smoke_test_file, 'w') as f:
    f.write(shebang)
    snippets_config = generate_config(config, query_template, f)
    f.write('\nprint("Smoke test complete!")')

  with open(output_file, 'w') as f:
    json.dump(snippets_config, f)

render_files(R_MENU_CONFIG, R_QUERY_TEMPLATE, R_JSON_OUTPUT,
             R_SHEBANG, R_SMOKE_TEST)
render_files(PY_MENU_CONFIG, PY_QUERY_TEMPLATE, PY_JSON_OUTPUT,
             PY_SHEBANG, PY_SMOKE_TEST)
