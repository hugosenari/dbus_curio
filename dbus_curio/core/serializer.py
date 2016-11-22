from struct import pack

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
    b'h': b'I',
    b's': b's',
    b'o': b's',
    b'g': b's',
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
    _pad = (window - (encoded_len % window)) * NULL
    if encoded_len < window:
        _pad = (window - encoded_len) * NULL
    return _pad


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


def serialize_struct(val, signture, endianess=LITLE_END):
    align_pad = ALIGN[b'('] * NULL
    b_val = b''
    for _val in val:
        b_val += serialize(signature, _val, endianess=endianess)
    return  align_pad + b_val


def serialize_dict(val, signture, endianess=LITLE_END):
    align_pad = ALIGN[b'{'] * NULL
    b_val = b''
    for _key, _val in val.items():
        b_val += serialize(signature[0], _key, endianess=endianess)
        b_val += serialize(signature[1], _val, endianess=endianess)
    return  align_pad + b_val


def serialize_list(val, signture, endianess=LITLE_END):    
    _len = len(val)
    fmt_e = ENDIANESS[endianess]
    fmt_l = TRANSLATION[b'u']
    align_pad = ALIGN[signture[0]] * NULL
    b_len = pack(fmt_e + fmt_l, l_b_val)
    b_val = b''
    for _val in val:
        b_val += serialize(signature, _val, endianess=endianess)
    return  b_len + align_pad + b_val


def serialize(signature, endianess=LITLE_END, *args):
    for sig in signature:
        pass
    return b''


def deserialize(signature, endianess=LITLE_END):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
