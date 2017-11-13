#!python

import getopt
from sonarcube import *


def print_help():
    print('usage: {} -n <name> -k <key> [-b <branch>] [-p]'.format(__file__))


project_name = ''
key_name = ''
branch_name = ''
set_as_private = False
sys_args = sys.argv[1:]
headers = {'Content-Type': 'application/json'}

try:
    opts, args = getopt.getopt(sys_args, "hn:k:b:p", ["help", "name=", "key=", "branch=", "private"])
except getopt.GetoptError:
    print_help()
    sys.exit(const.SYS_ERROR_INVALID_ARGS)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print_help()
        sys.exit()
    elif opt in ("-n", "--name"):
        project_name = arg
    elif opt in ("-k", "--key"):
        key_name = arg
    elif opt in ("-b", "--branch"):
        branch_name = arg
    elif opt in ("-p", "--private"):
        set_as_private = True

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
create_project(key=key_name, name=project_name, branch='')

###
# Adding of group - users
###
group_name = '{}-users'.format(key_name)
group_description = ''
group_permissions = ['codeviewer', 'scan', 'user', 'issueadmin']

create_project_group(project_key=key_name, name=group_name, description=group_description, permissions=group_permissions)

###
# Adding of group - admins
###
group_name = '{}-admins'.format(key_name)
group_description = ''
group_permissions = ['user', 'issueadmin', 'admin']

create_project_group(project_key=key_name, name=group_name, description=group_description, permissions=group_permissions)

###
# Adding of group - users
###
group_name = '{}-viewers'.format(key_name)
group_description = ''
group_permissions = ['codeviewer', 'user']

create_project_group(project_key=key_name, name=group_name, description=group_description, permissions=group_permissions)
