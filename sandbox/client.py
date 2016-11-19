from curio import run, spawn
from dbus_curio import auth, session_bus


async def echo_client():
    socket, flags = await session_bus()
    ok_data = await auth(socket, flags)
    print(ok_data)
    # await socket.sendall(b'oi', flags=flags)
    # response = await socket.recv(16384)
    # print(response)


if __name__ == '__main__':
    run(echo_client())
