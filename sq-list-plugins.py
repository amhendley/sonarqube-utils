#!python

import getopt

from common.sonarcube import *


def print_help():
    print('usage: {} [-i] [-p] [-u] [-a] [-h]'.format(__file__))


show_installed = False
show_pending = False
show_updates = False
show_available = False
sys_args = sys.argv[1:]
headers = {'Content-Type': 'application/json'}

try:
    opts, args = getopt.getopt(sys_args, "hipua", ["help", "installed", "pending", "updates", "available"])
except getopt.GetoptError:
    print_help()
    sys.exit(const.SYS_ERROR_INVALID_ARGS)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print_help()
        sys.exit()
    elif opt in ("-i", "--installed"):
        show_installed = True
    elif opt in ("-p", "--pending"):
        show_pending = True
    elif opt in ("-u", "--updates"):
        show_updates = True
    elif opt in ("-a", "--available"):
        show_available = True


show_all = (True if not show_available and not show_updates and not show_pending and not show_installed else False)

if show_all:
    show_installed = True
    show_pending = True
    show_updates = True
    show_available = True

show_plugin_list(installed=show_installed, pending=show_pending, updates=show_updates, available=show_available)
