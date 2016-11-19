from curio import run, spawn, open_unix_connection
from dbus_curio.core.bus_finder import session_info
from dbus_curio.core.auth import auths
from socket import SCM_CREDENTIALS, AF_UNIX
from os import getuid


async def echo_client(con_info):
    flags = SCM_CREDENTIALS if con_info.family == AF_UNIX else 0
    print('> Connect to ', con_info.address)
    socket = await open_unix_connection(con_info.address)
    await socket.sendall(b'\0', flags=flags)
    ok_data = await auth(socket, flags)
    print(ok_data)


async def auth(socket, flags=0):
    ok_data = b''
    gen = auths()
    command = next(gen)
    while True:
        await socket.sendall(command, flags=flags)
        if b'BEGIN' in command:
            break
        response = await socket.recv(16384)
        if b'OK ' in response:
            ok_data = response.strip().split()[-1]
        print('SEND: {}\nRESP: {}'.format(command.strip(), response.strip()))
        command = gen.send(response.strip())
    return ok_data
    

    # print('> try ANONYMOUS AUTH')
    # await client.sendall(b'AUTH ANONYMOUS 31303030\r\n', flags=flags)
    # print('> receive AUTH options')
    # resp = await client.recv(16384, flags=flags)
    # print(resp)
    # print('> try EXTERNAL AUTH')
    # await client.sendall(b'AUTH EXTERNAL\r\n', flags=flags)
    # print('> receive AUTH response')
    # resp = await client.recv(16384, flags=flags)
    # print(resp)
    # print('> Send DATA')
    # await client.sendall(b'DATA\r\n', flags=flags)
    # print('> receive OK')
    # resp = await client.recv(16384, flags=flags)
    # print(resp)
    # print('> Send BEGIN')
    # await client.sendall(b'BEGIN\r\n', flags=flags)
    #print('Connection closed')


if __name__ == '__main__':
    run(echo_client(session_info()))
