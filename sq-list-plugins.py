#!python

import argparse
import os

from common.sonarcube import *


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='Utility script to create a new project in SonarQube')

try:
    parser.add_argument('-i', '--installed', action='store_true',
                        help='List all the plugins installed, sorted by plugin name.')
    parser.add_argument('-p', '--pending', action='store_true',
                        help='List plugins which will either be installed or removed at the next startup, sorted by plugin name.')
    parser.add_argument('-u', '--updates', action='store_true',
                        help='List plugins installed which at least one newer version is available, sorted by plugin name.')
    parser.add_argument('-a', '--available', action='store_true',
                        help='List all the plugins available for installation, sorted by plugin name..')

    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

show_installed = args.installed
show_pending = args.pending
show_updates = args.updates
show_available = args.available
show_all = (True if not show_available and not show_updates and not show_pending and not show_installed else False)

if show_all:
    show_installed = True
    show_pending = True
    show_updates = True
    show_available = True

show_plugin_list(installed=show_installed, pending=show_pending, updates=show_updates, available=show_available)
