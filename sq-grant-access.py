#!/usr/bin/python

import argparse
import os

from common.sonarcube import *

parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='Utility script to grant user access to a project in SonarQube')

try:
    parser.add_argument('-l', '--login', required=True, help='The unique name of the login account')
    parser.add_argument('-n', '--name', required=True, help='The name description of the login account')
    parser.add_argument('-p', '--password', help='The password for the login account')
    parser.add_argument('-e', '--email', help='The email for the login account')
    parser.add_argument('-s', '--scm', nargs='*',
                        help='The SCM account name to be associated with the login account. Multiples allowed')
    parser.add_argument('-g', '--group', nargs='*',
                        help='The name of a group the user to be assigned to. Multiples allowed')
    parser.add_argument('-x', '--external', action='store_true',
                        help='Indicates whether the login account is external to SonarQube. The default is internal.')

    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

login_id = args.login
login_name = args.name
login_password = args.password
login_email = args.email
login_scm = args.scm
login_local = (not args.external)
project_key = args.key
groups = args.group

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

create_user(login=login_id,
            name=login_name,
            email=login_email,
            password=login_password,
            scm=login_scm,
            local=login_local)

for group in groups:
    add_group_user(group=group, login=login_id)
