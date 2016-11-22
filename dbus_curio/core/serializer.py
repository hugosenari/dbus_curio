from struct import pack

NULL = b'\x00'

HEADER_SIG = b'yyyyuua(yv)'
TRANSLATION = {
    b'y': b'b',
    b'b': b'?',
    b'n': b'h',
    b'q': b'H',
    b'i': b'i',
    b'u': b'I',
    b'x': b'q',
    b't': b'Q',
    b'd': b'd',
    b'h': b'I',
    b's': b's',
    b'o': b's',
    b'g': b's',
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
    pad = (window - (encoded_len % window)) * NULL
    if encoded_len < window:
        pad = (window - encoded_len) * NULL
    return pad


def serialize_msg(header, *body):
    header_bytes = bytes(header)
    body_bytes = serialize(header.signature, *body)
    return header_bytes + body_bytes


def serialize_str(val, signature=b's', endianess=LITLE_END):
    type_of_len = b'y' if signature == b'g' else b'u'
    fmt_e = ENDIANESS[endianess]
    fmt_l = TRANSLATION[type_of_len]
    b_val = val.encode(encoding='UTF-8')
    l_b_val = len(b_val)
    b_len = pack(fmt_e + fmt_l, l_b_val)
    b_pad = pad(l_b_val + 1) + NULL  # null-terminated string
    return b_len + b_val + b_pad


def serialize_var(val, signature, endianess=LITLE_END):
    _signature = serialize_str(signature, b'g', endianess)
    _val = serialize(signature, val, endianess=endianess)
    return _signature + _val


def serialize(signature, endianess=LITLE_END, *args):
    for c in signature:
        pass
    return b''


def deserialize(signature, endianess=LITLE_END):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
