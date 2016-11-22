from struct import pack
from uuid import uuid4
from collections import namedtuple
from enum import IntEnum


class Field(namedtuple('HeaderField', ['code', 'value'])):
    def __bytes__(self):
        pass


FIELD_SIGNATURE = [
    b'',
    b'o',
    b's',
    b's',
    b's',
    b'u',
    b's',
    b's',
    b'g',
    b'u'
]


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

    @property
    def signature(self):
        return FIELD_SIGNATURE[int(self)]

    def make(self, value):
        return Field(self, value)

    def __bytes__(self):
        return bytes([self.value])


class ToBytesMixIn(object):
    def encode_dbus(self, endianness=None):
        yield b''

    def __bytes__(self):
        return bytes(b''.join(self.encode_dbus()))


class Header(namedtuple('Header', [
        'endianness', 'message_type', 'flags',
        'version', 'length', 'serial', 'fields']), ToBytesMixIn):

    def encode_dbus(self, endianness=None):
        e = endianness or self.endianness
        fmt = Endianness.fmt_of(e)
        yield pack(fmt + b'bbbbII',
                   self.endianness.value,
                   self.message_type.value,
                   self.flags,
                   self.version,
                   self.length,
                   self.serial)

    def field(self, code):
        r = [x for x in self.fields if int(code) == x.code]
        if not len(r):
            return list(FieldCodes)[int(code)].make(b'')
        return r[0]

    @property
    def path(self):
        return self.field(FieldCodes.PATH)

    @property
    def interface(self):
        return self.field(FieldCodes.INTERFACE)

    @property
    def member(self):
        return self.field(FieldCodes.MEMBER)

    @property
    def error_name(self):
        return self.field(FieldCodes.ERROR_NAME)

    @property
    def reply_serial(self):
        return self.field(FieldCodes.REPLY_SERIAL)

    @property
    def destination(self):
        return self.field(FieldCodes.DESTINATION)

    @property
    def sender(self):
        return self.field(FieldCodes.SENDER)

    @property
    def signature(self):
        return self.field(FieldCodes.SIGNATURE)

    @property
    def unix_fds(self):
        return self.field(FieldCodes.UNIX_FDS)


class Endianness(IntEnum):
    LITTLE = 108
    BIG = 66

    def encode_dbus(self, endianness=None):
        e = endianness or self
        fmt = Endianness.fmt_of(e)
        yield pack(fmt + b'b', self.value)

    def __bytes__(self):
        return bytes(self.encode_dbus())

    @property
    def fmt(self):
        if self == Endianness.BIG:
            return b'>'
        return b'<'

    @staticmethod
    def of(val):
        if hasattr(val, 'endianness'):
            return Endianness.of(val.endianness)
        if val in (b'B', b'>', Endianness.BIG.value, Endianness.BIG):
            return Endianness.BIG
        return Endianness.LITTLE

    @staticmethod
    def fmt_of(val):
        if hasattr(val, 'fmt'):
            return val.fmt
        return Endianness.of(val).fmt


class MessageType(IntEnum):
    INVALID = 0
    METHOD_CALL = 1
    METHOD_RETURN = 2
    ERROR = 3
    SIGNAL = 4

    def encode_dbus(self, endianness=None):
        fmt = Endianness.fmt_of(endianness)
        yield pack(fmt+b'b', self.value)

    def __bytes__(self):
        return bytes(self.encode_dbus())


class Flags(IntEnum):
    NO_REPLY_EXPECTED = 0x1
    NO_AUTO_START = 0x2
    ALLOW_INTERACTIVE_AUTHORIZATION = 0x4

    @classmethod
    def all(cls):
        return 0x7

    def all_but(self):
        return bytes([Flags.all() ^ self])

    def encode_dbus(self, endianness=None):
        fmt = Endianness.fmt_of(endianness)
        yield pack(fmt+b'b', self.value)

    def __bytes__(self):
        return bytes(self.encode_dbus())


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
