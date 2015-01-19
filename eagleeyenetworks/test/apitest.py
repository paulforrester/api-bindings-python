from .. import *

_session = None
my_api_key = '00000000-1111-2222-3333-444444444444'


def do_auth_and_auth():
    global _session
    if not _session:
        _session = Session(my_api_key)
    authenticate_result = aaa.authenticate(_session, username='john@smith.com', password='blacksmithshitharder')
    return aaa.authorize(_session, token=authenticate_result.token)


def do_login():
    global _session
    if not _session:
        _session = Session(my_api_key)
    return aaa.login(_session, 'john@smith.com', 'blacksmithshitharder')


def do_logout():
    global _session
    if not _session:
        return
    aaa.logout(_session)


def get_device():
    global _session
    if not _session:
        raise APIConnectionError('No session exists')
    dev = Device.retrieve(_session, id='1000e7f1')
    return dev