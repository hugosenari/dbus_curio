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
