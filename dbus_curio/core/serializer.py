"""
================
DBus wire format
================

This module de/serialize objects from/to dbus wire format.

The spec for this code can be found here:
- https://dbus.freedesktop.org/doc/dbus-specification.html
- https://github.com/GNOME/glib/blob/master/gio/gdbusmessage.c

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
            ####                \x00\x00\x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x03
        VARIANT
            SIGNATURE           \x01\x73\x00
            SIZE                            \x12\x00\x00\x00
            VAL             \x63\x63\x63\x63\x63\x63\x63\x63
                            \x63\x63\x63\x63\x63\x63\x63\x63
                            \x63\x63\x00
            ####                        \x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x08
        VARIANT
            SIGNATURE           \x01\x67\x00
            SIZE                            \x0c
            VAL                                 \x74\x73\x6f
                            \x67\x79\x62\x6e\x71\x69\x75\x78
                            \x64\x00
            ####                    \x00\x00\x00\x00\x00\x00
    STRUCT
        BYTE                \x02
        VARIANT
            SIGNATURE           \x01\x73\x00
            SIZE                            \x11\x00\x00\x00
            VAL             \x62\x62\x62\x62\x62\x62\x62\x62
                            \x62\x2e\x62\x62\x62\x62\x62\x62
                            \x62\x00
            ####                    \x00\x00\x00\x00\x00\x00


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
    ####                    \x00\x00\x00
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

As you can see above #### is alingment 'hack' to meet dbus requirements.

There are 3 types of padding rules, ``container``, ``header``, ``body``


- Container:
    - Strings are aligned as multiple of 4;
    - Struct are aligned as multiple of 8;
    - Variant are aligned as multiple of 1;
    - Array aligned as multiple o content type.
        - Last object of array has no padding.
- Header:
    - "The length of the header must be a multiple of 8".
- Body:
    - Any value on body is aligned gloabally to message size at that point.
    - IE. see #### after BYTE and before BOOL, glib implementation is:
        - before put value see if current size meets the next value align;
        - put \x00 to fix it;
        - put value bytes;
        - https://dbus.freedesktop.org/doc/dbus-specification.html#idm601


OUTPUT:
-------

Glue all things and our message will be sent like this::

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
from collections import defaultdict
from .signature import break_signature


NULL = b'\x00'
EMPTY = b''
STRING = b's'
PATH = b'o'
SIGNATURE = b'g'
ARRAY = b'a'
STRUCT = b'('
DICT = b'{'
BYTE = b'y'
UINT32 = b'u'
CONTAINER = b'{(avsgo'
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
    b'v': 1,
    b'a': 4,
    b'(': 8,
    b'{': 8
}
LITLE_END = b'l'
BIG_END = b'B'
LITLE_END_FMT = b'<'
BIG_END_FMT = b'>'
_BIG_END = b'>B'
endian = lambda k:  BIG_END if k[0] in _BIG_END else LITLE_END 
_ENDIANESS = {LITLE_END: LITLE_END_FMT, BIG_END: BIG_END_FMT}
ENDIANESS = defaultdict(lambda:  LITLE_END, _ENDIANESS)


def pad(encoded_len, window=4):
    if encoded_len and encoded_len % window:
        if encoded_len < window:
            return NULL * (window - encoded_len) 
        else:
            return NULL * (encoded_len % window)
    return EMPTY


def has_next(it):
    try:
        return next(it)
    except StopIteration:
        return None


def join(val):
    return EMPTY.join(val)


def serialize_msg(header, *body):
    header_buf = join(header.encode_dbus())
    size = len(header_buf)
    body_it = serialize_body(size, header.signature, header.endianness, *body)
    body_buf = join(body_it)
    body_size = serialize_len(len(body_buf), endianess=header.endianness)
    yield join([header_buf[0:3], body_size, header_buf[7:]])
    yield pad(size, 8)
    yield body_buf


def serialize_body(header_size, signature, endianess=LITLE_END, *body):
    size = header_size
    signature_it = break_signature(signature)
    for arg in body:
        sig = next(signature_it)
        for b in serialize(sig, endianess, arg):
            yield pad(size, ALIGN[sig[0]])
            yield b
            size += len(b)


def serialize_str(val, signature=STRING, endianess=LITLE_END):
    type_of_len = BYTE if signature in SIGNATURE else UINT32
    b_val = val.encode(encoding='UTF-8')
    l_b_val = len(b_val)
    yield serialize_len(l_b_val, type_of_len, endianess)
    yield b_val + NULL  # null-terminated string
    yield pad(l_b_val + 1) if signature in (STRING, PATH) else EMPTY


def serialize_var(val, signature, endianess=LITLE_END):
    for b in serialize_str(signature, SIGNATURE, endianess):
        yield b
    for b in serialize(signature, endianess,  val):
        yield b


def serialize_struct(val, signature, endianess=LITLE_END):
    signature_it = break_signature(signature)
    for v in val:
        size = 0
        sig = next(signature_it)
        for b in serialize(sig, endianess, v):
            yield b
            size += len(b)
        yield pad(size, 8)


def serialize_dict(val, signature, endianess=LITLE_END):
    for _key, _val in val.items():
        size = 0
        for b in serialize(signature[0], endianess,  _key):
            yield b
            size += len(b)
        for b in serialize(signature[1], endianess,  _val):
            yield b
            size += len(b)
        yield pad(size, 8)


def serialize_list(val, signature, endianess=LITLE_END):
    sig = bytes([signature[0]])
    # empty
    if not val:  
        yield serialize_len(0, endianess=endianess)
    # simple type
    elif sig not in CONTAINER:
        yield serialize_len(len(val) * ALIGN[sig], endianess=endianess)
        yield pad(ALIGN[UINT32], ALIGN[sig])
        for v in val:
            for b in serialize(sig, endianess,  v):
                yield b
    # complex
    else:
        buf = []
        buf_size = 0
        it = iter(val)
        v = has_next(it)
        while v:
            _next = has_next(it)
            for item_buf in serialize(signature, endianess,  v):
                if _next or len(item_buf.strip(NULL)):
                    buf_size += len(item_buf)
                    buf.append(item_buf)
            v = _next
        yield serialize_len(buf_size, endianess=endianess)
        for b in buf:
            yield b


def serialize_len(size, signature=UINT32, endianess=LITLE_END):
    return pack(ENDIANESS[endianess] + TRANSLATION[signature], size)


def serialize(signature, endianess, *args):
    if not args:
        yield EMPTY
    signature_it = break_signature(signature)
    for arg in args:
        if hasattr(arg, 'encode_dbus'):
            for encoded in arg.encode_dbus(endianess):
                yield encoded
        else:
            sig = next(signature_it)
            fmt = TRANSLATION.get(sig)
            if fmt:
                end = ENDIANESS[endianess]
                yield pack(end + fmt, arg)
            elif sig in (STRING, PATH, SIGNATURE):
                for encoded in serialize_str(arg, sig, endianess):
                    yield encoded
            elif sig.startswith(ARRAY):
                for encoded in serialize_list(arg, sig[1:], endianess):
                    yield encoded
            elif sig.startswith(STRUCT):
                for encoded in serialize_struct(arg, sig[1:-1], endianess):
                    yield encoded
            elif sig.startswith(DICT):
                for encoded in serialize_dict(arg, sig[1:-1], endianess):
                    yield encoded


def deserialize(signature, endianess=LITLE_END):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
