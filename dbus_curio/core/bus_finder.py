from os import environ, path, walk
from socket import AF_INET, AF_INET6, AF_UNIX
from collections import namedtuple

SYSTEM_ENV = "DBUS_SYSTEM_BUS_ADDRESS"
SYSTEM_DEFAULT = 'unix:path=/var/run/dbus/system_bus_socket'
SESSION_ENV = "DBUS_SESSION_BUS_ADDRESS"
USER_DIR_CFG = '~/.dbus/session-bus'

_ConInfo = namedtuple('_ConInfo', [
        'address',
        'family',
        'port',
        'ssl',
        'local_addr'
    ]
)


class ConInfo(_ConInfo):
    def __new__(cls, address, family, port, ssl, local_addr):
        assert address
        assert family
        return _ConInfo.__new__(
            cls,
            address,
            family,
            port,
            ssl,
            local_addr
        )


class UnixConfInfo(ConInfo):
    def __new__(cls, address):
        return ConInfo.__new__(
            cls,
            address,
            AF_UNIX,
            None,
            False,
            None
        )


class ConInfoException(Exception):
    pass


class _BusFinder(object):
    def __init__(self, addr):
        self.addrs = [v for v in self._addr_info(addr)]

    def _addr_info(self, addr):
        addrs = addr.split(';')
        for address in addrs:
            con_type, params = address.split(':')
            info = {'type': con_type}
            for param in params.split(','):
                k, v = param.split('=')
                info[k] = v
            yield info

    @property
    def connection_info(self):
        for addr in self.addrs:
            if addr['type'] == 'unix':
                to = addr.get('path')
                to = to or addr.get('tmpdir')
                to = to or '\0' + addr.get('abstract')
                return UnixConfInfo(address=to)
            elif addr['type'] == 'launchd':
                env = addr.get('env')
                to = environ.get(env, None)
                return UnixConfInfo(address=to)
            elif addr['tcp'] == 'launchd':
                host = addr.get('host', '127.0.0.1')
                bind = addr.get('bind', None)
                port = addr.get('port', None)
                family = addr.get('family', None)
                return ConInfo(
                    address=host,
                    family=AF_INET6 if family == 'ipv6' else AF_INET,
                    port=port,
                    ssl=port == '443',
                    local_addr=bind
                )
        raise ConInfoException('UNKNOWN ADDRESS TYPE')


class _SystemFinder(_BusFinder):
    def __init__(self, addr=None):
        addr = addr or environ.get(SYSTEM_ENV, SYSTEM_DEFAULT)
        _BusFinder.__init__(self, addr)


class _SessionFinder(_BusFinder):
    def __init__(self, addr=None):
        addr = addr or environ.get(SESSION_ENV, None)
        addr = addr or self._get_adrr_from_file()
        _BusFinder.__init__(self, addr)

    def _get_adrr_from_file(self, userdir=USER_DIR_CFG):
        user_dir = path.expanduser(userdir)
        addr = None
        if path.exists(user_dir):
            if path.isdir(user_dir):
                addr = self._walk_dir_looking_for_addr(user_dir)
            else:
                addr = self._look_for_address(user_dir)
            if addr:
                return addr
        raise ConInfoException('SESSION ADDRESS NOT FOUND')

    def _look_for_address(self, file_name):
        with open(file_name) as bus_info:
            for line in bus_info:
                if line.startswith(SESSION_ENV):
                    return line.replace(SESSION_ENV + '=', '')

    def _walk_dir_looking_for_addr(self, dir_name):
        for dirname, dirnames, filenames in walk(dir_name):
            for filename in filenames:
                user_file = path.join(dirname, filename)
                addr = self._look_for_address(user_file)
                if addr:
                    return addr


def session_info(address=None):
    return _SessionFinder(address).connection_info


def system_info(address=None):
    return _SystemFinder(address).connection_info


__all__ = [ConInfo, ConInfoException, session_info, system_info]


if __name__ == '__main__':
    print("Session: ", session_info())
    print("System: ", system_info())
