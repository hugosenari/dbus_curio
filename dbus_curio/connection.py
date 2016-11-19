from curio import open_connection, open_unix_connection
from socket import SCM_CREDENTIALS, AF_UNIX
from .core.bus_finder import session_info, system_info


async def connection(con_info):
    flags = 0
    if con_info.family == AF_UNIX:
        socket = await open_unix_connection(con_info.address)
        flags = SCM_CREDENTIALS
    else:
        socket = await open_connection(con_info.address, con_info.port)
    await socket.sendall(b'\0', flags=flags)
    return socket, flags


async def session_bus():
    return await connection(session_info())


async def system_bus():
    return await connection(system_info())
