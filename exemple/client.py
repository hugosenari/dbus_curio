from curio import run
from dbus_curio import SessionBus
from dbus_curio.client import Method, Signal


async def dbus_hello_client_method(bus): 
    # create message
    helloWorld = Method("HelloWorld",
                        path="/remote/object/path",
                        iface="com.example.Sample",
                        bus=bus)
    # wait reply
    result = await helloWorld("Anon")
    #do something with response
    print(result)


async def dbus_hello_client_signal(bus):
    # define signal
    helloWorlded = Signal(
        "HelloWorlded",
        path="/remote/object/path",
        iface="com.example.Sample"
        bus=bus
    )    
    # wait signal
    result = await helloWorlded()
    #do something with response
    print(result)
    
async de dbus_hello_client(bus):
    await dbus_hello_client_method(bus)
    await dbus_hello_client_signal(bus)

if __name__ == "__main__":
    bus = SessionBus()
    run(dbus_hello_client(bus))