#!/usr/bin/python


import sys
import getopt
from common import *


def print_help():
    help_string = 'usage: {} -k <project_key> -g <group> [-d <group_description>] '.format(__file__)
    help_string += '-l <login> -n <name> -p <password> [-e <email>] [-s <scm_account>] [-x]'
    print(help_string)


project_key = ''
group_name = ''
group_description = ''
login_id = ''
login_name = ''
login_password = ''
login_email = ''
login_scm = []
login_local = 'true'
sys_args = sys.argv[1:]

try:
    opts, args = getopt.getopt(sys_args, "hk:g:d:l:n:p:e:s:x", ["help", "project-key=", "group=", "description=",
                                                                "login=", "name=", "password=", "email=", "scm=",
                                                                "external"])
except getopt.GetoptError:
    print_help()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print_help()
        sys.exit()
    elif opt in ("-k", "--project-key"):
        project_key = arg
    elif opt in ("-g", "--group"):
        group_name = arg
    elif opt in ("-d", "--description"):
        group_description = arg
    elif opt in ("-l", "--login"):
        login_id = arg
    elif opt in ("-n", "--name"):
        login_name = arg
    elif opt in ("-p", "--password"):
        login_password = arg
    elif opt in ("-e", "--email"):
        login_email = arg
    elif opt in ("-s", "--scm"):
        login_scm.append(arg)
    elif opt in ("-x", "--external"):
        login_local = 'false'

#
# SonarQube
# Structures:
#  Project (name, key, branch?, Public*|Private[v6+])
#  View (name, key) [Enterprise version]
#  Group (name, description?)
#  User (login, name, email?, password, scm_account?)
#
# Permissions:
#
#

url = base_url + 'user_groups/search'
params = {
    'f': 'name',
    'q': group_name
}

resp = requests.get(url=expand_url(url, params), auth=auth)

if resp.status_code != 200:
    print_response_error(resp)
    sys.exit(3)

msg = decode_json(resp.json())

# {u'paging': {u'pageIndex': 1, u'total': 2, u'pageSize': 100},
#   u'groups': [{u'default': False, u'id': 1, u'name': u'sonar-administrators'},
#               {u'default': True, u'id': 2, u'name': u'sonar-users'}]}
if msg['paging']['total'] == 0:
    url = base_url + 'user_groups/create'
    headers = {'Content-Type': 'application/json'}
    params = {
        'name': group_name,
        'description': group_description
    }
    url = expand_url(url, params)

    resp = requests.post(url=url, headers=headers, auth=auth)

    if resp.status_code != 200:
        print('Url : {}'.format(url))
        print_response_error(resp)
        sys.exit(4)
    else:
        print(pretty_print_json(resp.json()))


url = base_url + 'users/search'
params = {
    'q': login_id
}

resp = requests.get(url=expand_url(url, params), auth=auth)

if resp.status_code != 200:
    print_response_error(resp)
    sys.exit(5)

msg = decode_json(resp.json())

# {u'paging': {u'pageIndex': 1, u'total': 2, u'pageSize': 100},
#   u'groups': [{u'default': False, u'id': 1, u'name': u'sonar-administrators'},
#               {u'default': True, u'id': 2, u'name': u'sonar-users'}]}
if msg['paging']['total'] == 0:
    url = base_url + 'users/create'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': login_id,
        'name': login_name,
        'password': login_password,
        'email': login_email,
        'local': login_local
    }

    for scm in login_scm:
        params.items().append('scmAccount', scm)

    url = expand_url(url, params)

    resp = requests.post(url=url, headers=headers, auth=auth)

    if resp.status_code != 200:
        print('Url : {}'.format(url))
        print_response_error(resp)
        sys.exit(6)
    else:
        print(pretty_print_json(resp.json()))

    url = base_url + 'user_groups/add_user'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': login_id,
        'name': group_name
    }

    url = expand_url(url, params)
    resp = requests.post(url=url, headers=headers, auth=auth)
    if resp.status_code != 204:
        print('Url : {}'.format(url))
        print_response_error(resp)
        sys.exit(7)
    else:
        url = base_url + 'users/groups'
        params = {
            'login': login_id
        }

        resp = requests.get(url=expand_url(url, params), auth=auth)

        if resp.status_code != 200:
            print_response_error(resp)
            sys.exit(8)
        else:
            print(pretty_print_json(resp.json()))
