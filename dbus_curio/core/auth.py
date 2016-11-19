from os import getpid
from binascii import hexlify


class AuthException(Exception):
    pass


def external():
    resp = yield b'AUTH EXTERNAL'
    if b'DATA' in resp:
        resp = yield b'DATA'
    if b'OK ' in resp:
        resp = yield b'NEGOTIATE_UNIX_FD'
        resp = yield b'BEGIN'
    raise AuthException('Cannot authenticate with EXTERNAL')


def anonymous():
    pid = hexlify(str(getpid()).encode())
    resp = yield b'AUTH ANONYMOUS ' + pid
    if b'DATA' in resp:
        resp = yield b'DATA'
    if b'OK ' in resp:
        resp = yield b'BEGIN'
    raise AuthException('Cannot authenticate with ANONYMOUS')


AUTH_METHODS = {
    b'anonymous': anonymous,
    b'external': external
}


def auths(methods=AUTH_METHODS):
    response = yield b'AUTH\r\n'
    if not methods:
        raise AuthException('No auth method implementation defined')
    server_methods = response.strip().split(b' ')[1:]
    if not server_methods:
        raise AuthException('Server has no auth methods')
    for server_method in server_methods:
        method = methods.get(server_method.lower())
        try:
            if method:
                gen = method()
                command = next(gen)
                while True:
                    response = yield command + b'\r\n'
                    if b'BEGIN' in command:
                        break
                    command = gen.send(response.strip())
                else:
                    break
        except AuthException:
            pass
    raise AuthException('Cannot authenticate with defined methods')
