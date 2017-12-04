import json
import requests.auth
import requests
import sys
import urllib
import httplib
from termcolor import colored


class const:
    class ConstError(TypeError):
        pass

    def __init__(self):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError, "Can't unbind const(%s)" % name
        raise NameError, name


const = const()
const.SYS_ERROR_INVALID_ARGS = 2


def pretty_print_json(data):
    return json.dumps(data, indent=4, separators=(',', ':'))


def decode_json(data):
    return json.JSONDecoder().decode(pretty_print_json(data))


def print_error(msg):
    print(colored(msg, 'red'))


def print_response_error(response):
    msg = ''
    err = decode_json(response.json())
    for e in err['errors']:
        msg += '{}\n'.format(e['msg'])
    print_error('ERROR ({}) {}'.format(response.status_code, msg))


def expand_url(url, params={}):
    _url = url
    if params:
        _url += '?'
    _paramFormat = '{}={}&'

    for key, value in params.items():
        if isinstance(value, list):
            for value2 in value:
                _url += _paramFormat.format(key, urllib.quote_plus(str(value2)))
        else:
            _url += _paramFormat.format(key, urllib.quote_plus(str(value)))

    return _url


def send_request(url, auth, headers='', exit_value=None):
    print('Sending request to url : {}'.format(url))
    resp = requests.post(url=url, headers=headers, auth=auth)

    print('RESPONSE: {}'.format(resp.status_code))

    if resp.status_code >= httplib.BAD_REQUEST:
        if resp.json():
            print_response_error(resp)
        
        if exit_value:
            sys.exit(exit_value)
    else:
        if resp.status_code == httplib.OK:
            print('Response Content:')
            print(pretty_print_json(resp.json()))

    return resp


def get_paging_info(resp):
    msg = decode_json(resp.json())
    return msg['paging']['pageIndex'], msg['paging']['total'], msg['paging']['pageSize']


properties = json.load(file('sonarqube.json'))

base_url = properties['base_url']
# ref: https://docs.sonarqube.org/display/SONAR/User+Token
access_token = properties['access_token']
auth = requests.auth.HTTPBasicAuth(username=access_token, password='')
