from getpass import getuser
from binascii import hexlify, unhexlify
from hashlib import sha1
from os import urandom, path

COOKIE_DIR = '~/.dbus-keyrings'


class AuthException(Exception):
    pass


def _sha1(challenge, pass_, cookie):
    result = hexlify(sha1(b':'.join([challenge, pass_, cookie])).digest())
    return b' '.join([pass_, result])


def _dbus_gookie(context, uid, challenge):
    file_name = path.expanduser(path.join(COOKIE_DIR, context))
    pass_ = hexlify(sha1(urandom(8)).digest())
    try:
        with open(file_name, 'r') as file_:
            for line in file_:
                _uid, _time, _cookie = line.split()
                if uid == _uid:
                    return _sha1(challenge, pass_, _cookie)
            raise AuthException('DBUS_COOKIE_SHA1 cookie not found')
    except IOError as e:
        raise AuthException('DBUS_COOKIE_SHA1 cannot read cookie file', e)


def anonymous():
    user = hexlify(getuser().encode())
    resp = yield b'AUTH ANONYMOUS ' + user
    if b'DATA' in resp:
        resp = yield b'DATA'
    if b'OK ' in resp:
        resp = yield b'NEGOTIATE_UNIX_FD'
        resp = yield b'BEGIN'
    raise AuthException('Cannot authenticate with ANONYMOUS')


def dbus_cookie_sha1():
    user = hexlify(getuser().encode())
    resp = yield b'AUTH DBUS_COOKIE_SHA1 ' + user
    if b'DATA' in resp:
        data = unhexlify(resp.strip(b'DATA').strip())
        resp = yield b'DATA ' + hexlify(_dbus_gookie(*data.split()))
    if b'OK ' in resp:
        resp = yield b'NEGOTIATE_UNIX_FD'
        resp = yield b'BEGIN'
    raise AuthException('DBUS_COOKIE_SHA1 not implemented')


def external():
    resp = yield b'AUTH EXTERNAL'
    if b'DATA' in resp:
        resp = yield b'DATA'
    if b'OK ' in resp:
        resp = yield b'NEGOTIATE_UNIX_FD'
        resp = yield b'BEGIN'
    raise AuthException('Cannot authenticate with EXTERNAL')


AUTH_METHODS = {
    b'external': external,
    b'anonymous': anonymous,
    b'dbus_cookie_sha1': dbus_cookie_sha1
}


def auths(methods=None):
    _methods = methods or AUTH_METHODS
    response = yield b'AUTH\r\n'
    if not _methods:
        raise AuthException('No auth method implementation defined')
    server_methods = response.strip().split(b' ')[1:]
    if not server_methods:
        raise AuthException('Server has no auth methods')
    for server_method in server_methods:
        method = _methods.get(server_method.lower())
        try:
            if method:
                gen = method()
                command = next(gen)
                while True:
                    response = yield command + b'\r\n'
                    command = gen.send(response.strip())
        except AuthException:
            pass
    raise AuthException('Cannot authenticate with defined methods ({})'
                        .format(_methods.keys()))
