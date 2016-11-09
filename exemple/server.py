from curio import sleep, run, spawn
from dbus_curio import SessionBus
from dbus_curio.server import DefMethod, DefSignal


async def dbus_hello_server_method(bus): 
    # create message
    helloWorld = DefMethod("HelloWorld"
                            path="/remote/object/path",
                            iface="com.example.Sample",
                            params="s",
                            result="s",
                            bus=bus)
    while True
        # wait method_call
        method_call = await helloWorld()
        #do something with params
        print(method_call.args)
        #respond
        response = "Hello World {}".format(method_call.args[0])
        await method_call.respond(response)


async def dbus_hello_server_signal(bus):
    # define signal
    helloWorlded = DefSignal(
        "HelloWorlded",
        path="/remote/object/path",
        iface="com.example.Sample",
        result="s",
        bus=bus
    )
    # emit signal
    while True:
        await sleep(10)
        await helloWorlded("voodoo boo boo")

async def dbus_hello_server(bus):
    method_task = await spawn(dbus_hello_server_method(bus))
    signal_task = await spawn(dbus_hello_server_signal(bus))


if __name__ == "__main__":
    bus = SessionBus()
    run(dbus_hello_server(bus))