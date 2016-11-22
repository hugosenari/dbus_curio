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
    if encoded_len < window:
        return (window - encoded_len) * NULL
    return (window - (encoded_len % window)) * NULL


def serialize_msg(header, *body):
    for _header in header.encode_dbus():
        yield _header
    for _body in serialize(header.signature, *body):
        yield _body


def serialize_str(val, signature=b's', endianess=LITLE_END):
    type_of_len = b'y' if signature == b'g' else b'u'
    b_val = val.encode(encoding='UTF-8')
    l_b_val = len(b_val)
    yield pack(ENDIANESS[endianess] + TRANSLATION[type_of_len], l_b_val)
    yield b_val + NULL  # null-terminated string
    yield pad(l_b_val + 1)  # this 1 stands for null ending


def serialize_var(val, signature, endianess=LITLE_END):
    yield serialize_str(signature, b'g', endianess)
    yield serialize(signature, val, endianess=endianess)


def serialize_struct(val, signature, endianess=LITLE_END):
    yield ALIGN[b'('] * NULL
    for _val in val:
        yield serialize(signature, _val, endianess=endianess)


def serialize_dict(val, signature, endianess=LITLE_END):
    yield ALIGN[b'{'] * NULL
    for _key, _val in val.items():
        for b_key in serialize(signature[0], _key, endianess=endianess):
            yield b_key
        for b_val in serialize(signature[0], _val, endianess=endianess):
            yield b_val


def serialize_list(val, signature, endianess=LITLE_END):
    yield pack(ENDIANESS[endianess] + TRANSLATION[b'u'], len(val))
    yield ALIGN[signature[0]] * NULL
    for _val in val:
        for b_val in serialize(signature, _val, endianess=endianess):
            yield b_val


def end_of_struct(signature):
    return end_of(b'(', b')', signature)


def end_of_dict(signature):
    return end_of(b'{', b'}', signature)


def end_of_array(signature):
    b_c = bytes([signature[0]])
    if b_c == b'{':
        return b_c + end_of_dict(signature[1:])
    if b_c == b'(':
        return b_c + end_of_struct(signature[1:])
    if b_c == b'a':
        return b_c + end_of_array(signature[1:])
    return b_c


def end_of(begin, end, signature):
        count = 1
        result = b''
        for c in signature:
            b_c = bytes([c])
            result += b_c
            if b_c == begin:
                count += 1
            if b_c == end:
                count -= 1
            if not count:
                return result


def break_signature(signature):
    count = len(signature)
    i = -1
    b_c = b''
    skip = b''
    while True:
        i += 1
        if i > count:
            break
        b_c = bytes([signature[i]])
        if b_c in (b'a', b'(', b'{'):
            if b_c == b'(':
                skip = b_c + end_of_struct(signature[i + 1:])
            elif b_c == b'{':
                skip = b_c + end_of_dict(signature[i + 1:])
            elif b_c == b'a':
                skip = b_c + end_of_array(signature[i + 1:])
            i += len(skip)
            yield skip
        else:
            yield b_c


def serialize(signature, endianess=LITLE_END, *args):
    yield b''
    for arg in args:
        if hasattr(arg, 'encode_dbus'):
            for encoded in arg.encode_dbus(endianess):
                yield encoded
            raise StopIteration()
        else:
            TRANSLATION[signature[0]]


def deserialize(signature, endianess=LITLE_END):
    raise SerializeExeption('Deserialize method not implemented')


class SerializeExeption(Exception):
    pass
