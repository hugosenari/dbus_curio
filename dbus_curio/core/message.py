from collections import namedtuple
from enum import Enum, IntEnum

HeaderField = namedtuple('HeaderField', [
        'code',
        'value'
    ]
)

Header = namedtuple('Header', [
        'endianness',
        'message_type',
        'flags',
        'version',
        'length',
        'serial',
        'fields'
    ]
)


class Endianness(Enum):
    LITTLE = b'l'
    BIG = b'B'


class MessageType(IntEnum):
    INVALID = 0
    METHOD_CALL = 1
    METHOD_RETURN = 2
    ERROR = 3
    SIGNAL = 4


class Flags(IntEnum):
    NO_REPLY_EXPECTED = 0x1
    NO_AUTO_START = 0x2
    ALLOW_INTERACTIVE_AUTHORIZATION = 0x4

    @classmethod
    def all(cls):
        return 0x7

    def all_but(self):
        return Flags.all() ^ self


class HeaderFieldCodes(IntEnum):
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
        return HeaderField(self.value, value)
