from struct import pack
from uuid import uuid4
from collections import namedtuple
from enum import IntEnum


class Field(namedtuple('HeaderField', ['code', 'value'])):
    def __bytes__(self):
        pass


class Header(namedtuple('Header', [
        'endianness', 'message_type', 'flags',
        'version', 'length', 'serial', 'fields'])):

    def __bytes__(self):
        header_fmt = self.endianness.fmt + b'bbbbII'
        header_bytes = pack(header_fmt,
                            self.endianness,
                            self.message_type,
                            self.flags,
                            self.version,
                            self.length,
                            self.serial)
        return bytes(header_bytes)


class Endianness(IntEnum):
    LITTLE = ord(b'l')
    BIG = ord(b'B')

    def __bytes__(self):
        return chr(self.value).encode()

    @property
    def fmt(self):
        if self == Endianness.BIG:
            return b'>'
        return b'<'


class MessageType(IntEnum):
    INVALID = 0
    METHOD_CALL = 1
    METHOD_RETURN = 2
    ERROR = 3
    SIGNAL = 4

    def __bytes__(self):
        return bytes([self.value])


class Flags(IntEnum):
    NO_REPLY_EXPECTED = 0x1
    NO_AUTO_START = 0x2
    ALLOW_INTERACTIVE_AUTHORIZATION = 0x4

    @classmethod
    def all(cls):
        return 0x7

    def all_but(self):
        return bytes([Flags.all() ^ self])

    def __bytes__(self):
        return bytes([self.value])


class FieldCodes(IntEnum):
    INVALID = 0
    PATH = 1
    INTERFACE = 2
    MEMBER = 3
    ERROR_NAME = 4
    REPLY_SERIAL = 5
    DESTINATION = 6
    SENDER = 7
    SIGNATURE = 8
    UNIX_FDS = 9

    def make(self, value):
        return Field(self, value)

    def __bytes__(self):
        return bytes([self.value])


def header(message_type,
           serial=None, length=0, endianness=None,
           flags=None, version=1,
           **fields):
    _fields = [FieldCodes[key.upper()].make(value)
               for key, value in fields.items() if value]
    return Header(
        endianness or Endianness.LITTLE,
        message_type,
        flags or 0,
        version or 1,
        length,
        serial or uuid4().int,
        _fields)


def method_call(path, member, interface=None, signature=None,
                serial=None, length=0, endianness=None,
                flags=None, version=1):
    fields = {
        'path': path,
        'member': member,
        'interface': interface,
        'signature': signature
    }
    return header(
        MessageType.METHOD_CALL,
        serial, length, endianness, flags, version,
        **fields
    )


def method_return(reply_serial, signature=None,
                  serial=None, length=0, endianness=None,
                  flags=None, version=1):
    fields = {
        'reply_serial': reply_serial,
        'signature': signature
    }
    return header(
        MessageType.METHOD_RETURN,
        serial, length, endianness, flags, version,
        **fields
    )


def error(name, reply_serial, signature=None,
          serial=None, length=0, endianness=None,
          flags=None, version=1):
    fields = {
        'reply_serial': reply_serial,
        'signature': signature
    }
    return header(
        MessageType.ERROR,
        serial, length, endianness, flags, version,
        **fields
    )


def signal(path, member, interface=None, signature=None,
           serial=None, length=0, endianness=None,
           flags=None, version=1):
    fields = {
        'path': path,
        'member': member,
        'interface': interface,
        'signature': signature
    }
    return header(
        MessageType.SIGNAL,
        serial, length, endianness, flags, version,
        **fields
    )
