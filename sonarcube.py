
from common import *
import httplib


headers = {'Content-Type': 'application/json'}

const.SYS_ERROR_SEARCH_PROJECT = 3
const.SYS_ERROR_CREATE_PROJECT = 4


def create_project(key, name, branch):
    params = {
        'projects': key
    }
    resp = requests.get(url=expand_url(base_url + 'projects/search', params), auth=auth)

    if resp.status_code != httplib.OK:
        print_response_error(resp)
        sys.exit(const.SYS_ERROR_SEARCH_PROJECT)

    page_index, page_count, page_length = get_paging_info(resp)
    if page_count == 0:
        params = {
            'name': name,
            'project': key,
            'branch': branch
        }
        url = expand_url(base_url + 'projects/create', params)
        resp = requests.post(url=url, headers=headers, auth=auth)

        if resp.status_code != httplib.OK:
            print('Url : {}'.format(url))
            print_response_error(resp)
            sys.exit(const.SYS_ERROR_CREATE_PROJECT)
        else:
            print(pretty_print_json(resp.json()))


def create_project_group(project_key, name, description, permissions=[]):
    params = {
        'q': name
    }
    url = expand_url(base_url + 'user_groups/search', params)

    resp = send_request(url=url, headers=headers, auth=auth)
    page_index, page_count, page_length = get_paging_info(resp)

    if page_count == 0:
        params = {
            'name': name,
            'description': description
        }
        url = expand_url(base_url + 'user_groups/create', params)

        send_request(url=url, headers=headers, auth=auth)

    params = {
        'groupName': name,
        'projectKey': project_key,
        'permission': ''
    }
    for perm in permissions:
        params['permission'] = perm
        url = expand_url(base_url + 'permissions/add_group', params)
        send_request(url=url, headers=headers, auth=auth)


def show_plugin_list(installed, pending, updates, available):
    results = {
        installed: [],
        updates: [],
        pending: [],
        available: []
    }

    if installed:
        print("Installed:")
        print("  The list of all the plugins installed on the SonarQube instance, sorted by plugin name.")
        url = expand_url(base_url + 'plugins/installed')
        resp = send_request(url=url, headers=headers, auth=auth)

        if resp.status_code == httplib.OK:
            results['installed'] = decode_json(resp.json())['plugins']

    if updates:
        print("Updates:")
        print("  The list of plugins installed on the SonarQube instance for which at least one newer version is available, sorted by plugin name.")
        url = expand_url(base_url + 'plugins/updates')
        resp = send_request(url=url, headers=headers, auth=auth)

        if resp.status_code == httplib.OK:
            results['updates'] = decode_json(resp.json())['plugins']

    if pending:
        print("Pending:")
        print("  The list of plugins which will either be installed or removed at the next startup of the SonarQube instance, sorted by plugin name.")
        url = expand_url(base_url + 'plugins/pending')
        resp = send_request(url=url, headers=headers, auth=auth)

        if resp.status_code == httplib.OK:
            results['pending'] = decode_json(resp.json())['installing']

    if available:
        print("Available:")
        print("  The list of all the plugins available for installation on the SonarQube instance, sorted by plugin name.")
        url = expand_url(base_url + 'plugins/available')
        resp = send_request(url=url, headers=headers, auth=auth)

        if resp.status_code == httplib.OK:
            results['available'] = decode_json(resp.json())['plugins']

    return results
