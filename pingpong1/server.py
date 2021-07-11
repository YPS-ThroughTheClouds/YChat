import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import ServerBox
from utils import Server, localhost, port
from server_student import server_sends_a_pong

global ping
global pong


async def pingpong_socket_handler(reader, writer):
    server = Server(reader, writer)

    while True:
        msg = await server.receive_message()
        if msg == "Ping":
            with ping:
                ping.notify()

            with pong:
                pong.wait()

            await server_sends_a_pong(server, msg)


def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    pong_wnd = ServerBox(rt, lambda: print('Pong!'), ping, pong)
    rt.mainloop()


def start_asyncio():
    loop = asyncio.get_event_loop()
    core = asyncio.start_server(pingpong_socket_handler, localhost, port, loop=loop)
    server = loop.run_until_complete(core)
    # Serve requests until Ctrl+C is pressed

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    ping = Condition()
    pong = Condition()

    # Create and start gui
    start_gui(ping, pong)
    asyncio_thread = Thread(target=start_asyncio, daemon=True)