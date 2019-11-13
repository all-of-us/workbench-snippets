"""Auto-generate All of Us configuration for Jupyter 'Snippets Menu' extension.

Additionally, create smoke test scripts for both R and Python that include all
the snippets.

See also: https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/snippets_menu/readme.html
"""

import glob
import jinja2
import json
import os
import yaml

# Input file directory.
SNIPPETS_ROOT = '../'

R_QUERY_TEMPLATE = '''
{{ dataframe }} <- bq_table_download(bq_project_query(
    BILLING_PROJECT_ID, page_size = 25000,
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
        # It's a non-sql file, just read it in.
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
                 smoke_test_setup_file, smoke_test_file):
  """Use configuration to drive the autogeneration of snippets and tests."""
  with open(config_file, 'r') as f:
    config = yaml.load(f.read())

  print(yaml.dump(config))

  with open(smoke_test_file, 'w') as f:
    with open(smoke_test_setup_file, 'r') as setup_f:
      f.write(setup_f.read())
    snippets_config = generate_config(config, query_template, f)
    f.write('\nprint("Smoke test complete!")')

  with open(output_file, 'w') as f:
    json.dump(snippets_config, f)

for r_yaml in glob.glob('r_*.yml'):
  render_files(
    config_file=r_yaml,
    query_template=R_QUERY_TEMPLATE,
    output_file=r_yaml.replace('.yml', '.json'),
    smoke_test_setup_file=r_yaml.replace('.yml', '.smoke_test_setup'),
    smoke_test_file=r_yaml.replace('.yml', '_smoke_test.R'),
    )

for py_yaml in glob.glob('py_*.yml'):
  render_files(
    config_file=py_yaml,
    query_template=PY_QUERY_TEMPLATE,
    output_file=py_yaml.replace('.yml', '.json'),
    smoke_test_setup_file=py_yaml.replace('.yml', '.smoke_test_setup'),
    smoke_test_file=py_yaml.replace('.yml', '_smoke_test.py'),
    )
    
