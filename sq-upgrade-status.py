#!python

import argparse
import os

from common.sonarcube import *


parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 description='Utility script to capture the current status of SonarQube')

try:
    args = parser.parse_args()
except:
    sys.exit()

try:
    resp = get_server_status()

    if resp.status_code == httplib.OK:
        msg = decode_json(resp.json())

        print('SonarQube version is {}'.format(colored(msg['version'], 'blue')))

        if msg['status'] == 'STARTING':
            print('SonarQube Web Server is up and serving some Web Services (eg. api/system/status) but initialization is still ongoing')
        elif msg['status'] == 'UP':
            print('SonarQube instance is up and running')
        elif msg['status'] == 'DOWN':
            print('SonarQube instance is up but not running because migration has failed (refer to WS /api/system/migrate_db for details) or some other reason (check logs).')
        elif msg['status'] == 'RESTARTING':
            print('SonarQube instance is still up but a restart has been requested (refer to WS /api/system/restart for details).')
        elif msg['status'] == 'DB_MIGRATION_NEEDED':
            print('database migration is required. DB migration can be started using WS /api/system/migrate_db.')
        elif msg('status') == 'DB_MIGRATION_RUNNING':
            print('DB migration is running (refer to WS /api/system/migrate_db for details)')
except requests.exceptions.ConnectionError, ex:
    print_error('\nERROR: {}'.format(ex.message))
    sys.exit(1)
