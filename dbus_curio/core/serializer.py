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
ENDIANESS = {
    b'l': b'<',
    b'B': b'>'
}


def serialize_msg(header, *body):
    return bytes(header)
    header_bytes = bytes(header)
    return header_bytes


def pad(encoded_len, window=4):
    pad = (encoded_len % window) * NULL
    if encoded_len < window:
        pad = (window - encoded_len) * NULL
    return pad


def serialize_str(val, type_of_len=b'u', endianess=b'l'):
    fmt_e = ENDIANESS[endianess]
    fmt_l = TRANSLATION[type_of_len]
    b_val = val.encode(encoding='UTF-8') + NULL
    l_b_val = len(b_val)
    b_pad = pad(l_b_val)
    b_len = pack(fmt_e + fmt_l, l_b_val)
    if fmt_e == b'<':
        return b_pad + b_val + b_len
    return b_len + b_val + b_pad


def serialize(signature, *args):
    for c in signature:
        pass

    return b''


def deserialize(signature=HEADER_SIG, endianess=b'l'):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
