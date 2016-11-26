"""
================
DBus wire format
================

This module de/serialize objects from/to dbus wire format.

The spec for this code can be found here:
https://dbus.freedesktop.org/doc/dbus-specification.html#message-protocol-marshaling

Also this content helped:
https://people.gnome.org/~desrt/gvariant-serialisation.pdf

But if you are like me that prefer some samples here they are.

Our example is a complete DBus Message: *yyyyuua(yv)*``tsogybnqiuxd``


Header:
-------

DBus specs define message header as **yyyyuua(yv)** or
``BYTE, BYTE, BYTE, BYTE, UINT32, UINT32, ARRAY of STRUCT of (BYTE,VARIANT)``::

BYTE                    \x6c
BYTE                    \x04
BYTE                    \x01
BYTE                    \x01
UINT32                  \x60\x00\x00\x00
UINT32                  \x40\x00\x00\x00
ARRAY
    SIZE                \x72\x00\x00\x00
    STRUCT
        BYTE                \x01
        VARIANT
            SIGNATURE           \x01\x6f\x00
            SIZE                            \x10\x00\x00\x00
            VAL             \x2f\x61\x61\x61\x61\x61\x61\x61
                            \x2f\x61\x61\x61\x61\x61\x61\x61
                            \x00
            PADD                \x00\x00\x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x03
        VARIANT
            SIGNATURE           \x01\x73\x00
            SIZE                            \x12\x00\x00\x00
            VAL             \x63\x63\x63\x63\x63\x63\x63\x63
                            \x63\x63\x63\x63\x63\x63\x63\x63
                            \x63\x63\x00
            PADD                        \x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x08
        VARIANT
            SIGNATURE           \x01\x67\x00
            SIZE                            \x0c
            VAL                                 \x74\x73\x6f
                            \x67\x79\x62\x6e\x71\x69\x75\x78
                            \x64\x00
            PADD                    \x00\x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x02
        VARIANT
            SIGNATURE           \x01\x73\x00
            SIZE                            \x11\x00\x00\x00
            VAL             \x62\x62\x62\x62\x62\x62\x62\x62
                            \x62\x2e\x62\x62\x62\x62\x62\x62
                            \x62\x00
            PADD                    \x00\x00\x00\x00\x00\x00


- Our first byte define endianess ``\\x6c`` ('l', little-endian);
- The second byte is message type ``\\x04X`` (4, SIGNAL);
- Third byte ``\\x01`` (1, NO_REPLY_EXPECTED) are our header flags;
- Other byte for ``\\x01`` for protocol version;
- A UINT64 ``\\x60\\x00\\x00\\x00`` (240) with size of body in bytes;
- Another UINT64 ``\\x40\\x00\\x00\\x00`` message unique serial number;
- And last part ARRAY of STRUCT of (BYTE,VARIANT) message type fields:
    - ``\x72\x00\x00\x00`` UINT32 array size in bytes;
    - Struct with byte, variant:
        - ``\x01`` byte define header information field; 
        - Variant:
            - Variant signature:
                -``\x01`` signature size
                -``0x6f\x00`` signature val (`s`, string)
            - Variant content:
                - ``\x10\x00\x00\x00`` byte size of string;
                - ``\x2f\x61\x61...`` String value


Message body:
-------------

To be simple I defined our message body is defined as ``tsogybnqiuxd``:

UINT64                  \xff\xff\xff\xff
                        \xff\xff\xff\xff
STRING
    SIZE                \x10\x00\x00\x00
    VAL                 \x74\x68\x69\x73
                        \x20\x69\x73\x20
                        \x61\x20\x73\x74
                        \x72\x69\x6e\x67
                        \x00
    PADD                    \x00\x00\x00
PATH
    SIZE                \x0f\x00\x00\x00
    VAL                 \x2f\x74\x68\x69
                        \x73\x2f\x69\x73
                        \x2f\x61\x2f\x70
                        \x61\x74\x68\x00
SIGN
    SIZE                \x03
    VAL                     \x73\x61\x64
                        \x00
BYTE                        \x2a
####                            \x00\x00
BOOL                    \x01\x00\x00\x00
INT16                   \xd6\xff
UINT16                          \x60\xea
INT32                   \xd4\xff\xff\xff
UINT32                  \xa0\x86\x01\x00
INT64                   \xff\xff\xff\xff
                        \xff\xff\xff\xff
DOUB                    \x00\x00\x00\x00
                        \x00\x40\x45\x40


PADDING:
--------

There are 3 types of padding rules, ``container``, ``header``, ``body``


- Container:
    - Strings are aligned as multiple of 4
    - Struct are aligned as multiple of 8
    - Variant are alig as mutiple of 1
- Header:
    - "The length of the header must be a multiple of 8"    


- Body:
    - Is aligned gloabally (message size at that point)

OUTPUT:
-------

The glue all things and our message will be sent like this::

\x6c\x04\x01\x01\x60\x00\x00\x00
\x40\x00\x00\x00\x72\x00\x00\x00
\x08\x01\x67\x00\x0c\x74\x73\x6f
\x67\x79\x62\x6e\x71\x69\x75\x78
\x64\x00\x00\x00\x00\x00\x00\x00
\x01\x01\x6f\x00\x10\x00\x00\x00
\x2f\x61\x61\x61\x61\x61\x61\x61
\x2f\x61\x61\x61\x61\x61\x61\x61
\x00\x00\x00\x00\x00\x00\x00\x00
\x03\x01\x73\x00\x12\x00\x00\x00
\x63\x63\x63\x63\x63\x63\x63\x63
\x63\x63\x63\x63\x63\x63\x63\x63
\x63\x63\x00\x00\x00\x00\x00\x00
\x02\x01\x73\x00\x11\x00\x00\x00
\x62\x62\x62\x62\x62\x62\x62\x62
\x62\x2e\x62\x62\x62\x62\x62\x62
\x62\x00\x00\x00\x00\x00\x00\x00
\xff\xff\xff\xff\xff\xff\xff\xff
\x10\x00\x00\x00\x74\x68\x69\x73
\x20\x69\x73\x20\x61\x20\x73\x74
\x72\x69\x6e\x67\x00\x00\x00\x00
\x0f\x00\x00\x00\x2f\x74\x68\x69
\x73\x2f\x69\x73\x2f\x61\x2f\x70
\x61\x74\x68\x00\x03\x73\x61\x64
\x00\x2a\x00\x00\x01\x00\x00\x00
\xd6\xff\x60\xea\xd4\xff\xff\xff
\xa0\x86\x01\x00\xff\xff\xff\xff
\xff\xff\xff\xff\x00\x00\x00\x00
\x00\x40\x45\x40



"""

from struct import pack
from .signature import break_signature


NULL = b'\x00'
TRANSLATION = {
    b'y': b'b',
    b'b': b'I',
    b'n': b'h',
    b'q': b'H',
    b'i': b'i',
    b'u': b'I',
    b'x': b'q',
    b't': b'Q',
    b'd': b'd',
    b'h': b'I'
}
ALIGN = {
    b'y': 1,
    b'b': 4,
    b'n': 2,
    b'q': 2,
    b'i': 4,
    b'u': 4,
    b'x': 8,
    b't': 8,
    b'd': 8,
    b'h': 4,
    b's': 4,
    b'o': 4,
    b'g': 1,
    b'a': 4,
    b'(': 8,
    b'{': 8,
}
LITLE_END = b'l'
BIG_END = b'B'
LITLE_END_FMT = b'<'
BIG_END_FMT = b'>'
ENDIANESS = {
    LITLE_END: LITLE_END_FMT,
    BIG_END: BIG_END_FMT
}


def pad(encoded_len, window=4):
    if encoded_len < window:
        return (window - encoded_len) * NULL
    return (window - (encoded_len % window)) * NULL


def serialize_msg(header, *body):
    for _header in header.encode_dbus():
        yield _header
    for _body in serialize(header.signature, header.endianness, *body):
        yield _body


def serialize_str(val, signature=b's', endianess=LITLE_END):
    type_of_len = b'y' if signature == b'g' else b'u'
    b_val = val.encode(encoding='UTF-8')
    l_b_val = len(b_val)
    yield pack(ENDIANESS[endianess] + TRANSLATION[type_of_len], l_b_val)
    yield b_val + NULL  # null-terminated string
    yield pad(l_b_val + 1)  # + 1 for null ending


def serialize_var(val, signature, endianess=LITLE_END):
    yield serialize_str(signature, b'g', endianess)
    yield serialize(signature, endianess,  val)


def serialize_struct(val, signature, endianess=LITLE_END):
    yield ALIGN[b'('] * NULL
    for _val in val:
        yield serialize(signature, _val, endianess=endianess)


def serialize_dict(val, signature, endianess=LITLE_END):
    yield ALIGN[b'{'] * NULL
    for _key, _val in val.items():
        for b_key in serialize(signature[0], endianess,  _val):
            yield b_key
        for b_val in serialize(signature[0], endianess,  _val):
            yield b_val


def serialize_list(val, signature, endianess=LITLE_END):
    yield pack(ENDIANESS[endianess] + TRANSLATION[b'u'], len(val))
    yield ALIGN[signature[0]] * NULL
    for _val in val:
        for b_val in serialize(signature, endianess,  _val):
            yield b_val


def serialize(signature, endianess, *args):
    end = ENDIANESS[endianess]
    signature_it = break_signature(signature)
    for arg in args:
        if hasattr(arg, 'encode_dbus'):
            for encoded in arg.encode_dbus(endianess):
                yield encoded
        else:
            sig = next(signature_it)
            fmt = TRANSLATION.get(sig)
            if fmt:
                yield pack(end + fmt, arg)
            elif sig in (b's', b'o', b'g'):
                for encoded in serialize_str(arg, sig, endianess):
                    yield encoded
            elif sig.startswith(b'a'):
                for encoded in serialize_list(arg, sig[1:], endianess):
                    yield encoded
            elif sig.startswith(b'('):
                for encoded in serialize_struct(arg, sig[1:], endianess):
                    yield encoded
            elif sig.startswith(b'{'):
                for encoded in serialize_dict(arg, sig[1:], endianess):
                    yield encoded
            else:
                yield b''


def deserialize(signature, endianess=LITLE_END):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
