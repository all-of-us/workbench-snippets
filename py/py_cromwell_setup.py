import os
import subprocess
import json
import requests
from pathlib import Path

def check_for_app(env):
    list_apps_url = f'{env["leonardo_url"]}/api/google/v1/apps/{env["google_project"]}'
    r = requests.get(
        list_apps_url,
        params={
          'includeDeleted': 'false'
        },
        headers = {
            'Authorization': f'Bearer {env["token"]}'
        }
    )
    r.raise_for_status()

    for potential_app in r.json():
        if potential_app['appType'] == 'CROMWELL' and (
                str(potential_app['auditInfo']['creator']) == env['owner_email']
                or str(potential_app['auditInfo']['creator']) == env['user_email']
        ) :
            potential_app_name = potential_app['appName']
            potential_app_status = potential_app['status']

            # We found a CROMWELL app in the correct google project and owned by the user. Now just check the workspace:
            _, workspace_namespace,  proxy_url = get_app_details(env, potential_app_name)
            if workspace_namespace == env['workspace_namespace']:
                return potential_app_name, potential_app_status, proxy_url['cromwell-service']

    return None, None

def get_app_details(env, app_name):
    get_app_url = f'{env["leonardo_url"]}/api/google/v1/apps/{env["google_project"]}/{app_name}'
    print('start')
    r = requests.get(
        get_app_url,
        params={
            'includeDeleted': 'true'
        },
        headers={
            'Authorization': f'Bearer {env["token"]}'
        }
    )
    if r.status_code == 404:
        return 'DELETED', None, None, None
    else:
        r.raise_for_status()
    result_json = r.json()
    custom_environment_variables = result_json['customEnvironmentVariables']
    return result_json['status'], custom_environment_variables['WORKSPACE_NAMESPACE'], result_json.get('proxyUrls')

# Checks that cromshell is installed. Otherwise raises an error.
def validate_cromshell():
    print('Scanning for cromshell 2...')
    validate_command = subprocess.run(['cromshell-alpha', 'version'], capture_output=True, check=True, encoding='utf-8')
    version = str.strip(validate_command.stderr).split(' cromshell ')[-1]
    print(f'Cromshell 2 version detected: {version}')

def configure_cromwell(env, proxy_url):
     print('Updating cromwell config')
     file = f'{str(Path.home())}/.cromshell/cromshell_config.json'
     configuration = {
        'cromwell_server': proxy_url.split("swagger/", 1)[0],
        'requests_timeout': 5,
        'gcloud_token_email': env['user_email'],
        'referer_header_url': env['referer']
     }
     with open(file, 'w') as filetowrite:
        filetowrite.write(json.dumps(configuration, indent=2))

def find_app_status(env):
    print(f'Checking status for CROMWELL app')
    app_name, app_status, proxy_url = check_for_app(env)

    print(f'app_name={app_name}; app_status={app_status}')

    if app_name is None:
        print(f'CROMWELL app does not exist. Please create cromwell server from workbench')
    else:
        print(f'Existing CROMWELL app found (app_name={app_name}; app_status={app_status}).')
        configure_cromwell(env, proxy_url)
        exit(1)

def main():
    # Iteration 1: these ENV reads will throw errors if not set.
    env = {
        'workspace_namespace': os.environ['WORKSPACE_NAMESPACE'],
        'workspace_name': os.environ['WORKSPACE_NAME'],
        'workspace_bucket': os.environ['WORKSPACE_BUCKET'],
        'user_email': os.environ.get('PET_SA_EMAIL', default = os.environ['OWNER_EMAIL']),
        'owner_email': os.environ['OWNER_EMAIL'],
        'google_project': os.environ['GOOGLE_PROJECT'],
        'leonardo_url': os.environ['LEONARDO_BASE_URL'],
        'referer': os.environ['AOU_REFERER']
    }

    # Before going any further, check that cromshell2 is installed:
    validate_cromshell()

    # Fetch the token:
    token_fetch_command = subprocess.run(['gcloud', 'auth', 'print-access-token', env['user_email']], capture_output=True, check=True, encoding='utf-8')
    env['token'] = str.strip(token_fetch_command.stdout)

    find_app_status(env)


if __name__ == '__main__':
    main()