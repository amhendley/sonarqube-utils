#!python

import argparse
import os
from sonarcube import *


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='Utility script to create a new project in SonarQube')

try:
    parser.add_argument('-n', '--name', help='The name of the project to create')
    parser.add_argument('-k', '--key', help='The unique key of the project to create')
    parser.add_argument('-b', '--branch', help='The name of the branch the project needs associated with it')
    parser.add_argument('-p', '--private', action='store_true',
                        help='Indicates whether the project should be created as private. The default is public.')

    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

project_name = args.name
key_name = args.key
branch_name = args.branch
set_as_private = args.private
headers = {'Content-Type': 'application/json'}

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
