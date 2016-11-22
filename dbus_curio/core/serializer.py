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
