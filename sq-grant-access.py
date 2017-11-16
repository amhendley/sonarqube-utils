#!/usr/bin/python

import getopt
from sonarcube import *


def print_help():
    help_string = 'usage: {} -k <project_key> -g <group> '.format(__file__)
    help_string += '-l <login> -n <name> -p <password> [-e <email>] [-s <scm_account>] [-x]'
    print(help_string)


project_key = ''
groups = []
login_id = ''
login_name = ''
login_password = ''
login_email = ''
login_scm = []
login_local = 'true'
sys_args = sys.argv[1:]

try:
    opts, args = getopt.getopt(sys_args, "hk:g:d:l:n:p:e:s:x", ["help", "project-key=", "group=",
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
        groups.append(arg)
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

create_user(login=login_id,
            name=login_name,
            email=login_email,
            password=login_password,
            scm=login_scm,
            local=login_local)

for group in groups:
    add_group_user(group=group, login=login_id)
