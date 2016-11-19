from .core.auth import auths


async def auth(socket, flags=0):
    ok_data = b''
    gen = auths()
    command = next(gen)
    while True:
        await socket.sendall(command, flags=flags)
        if b'BEGIN' in command:
            break
        response = await socket.recv(16384)
        print('SEND: {}\nRESP: {}'.format(command.strip(), response.strip()))
        if b'OK ' in response:
            ok_data = response.strip().strip(b'OK ')
        command = gen.send(response.strip())
    return ok_data
