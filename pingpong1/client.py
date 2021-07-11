import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import ClientBox
from utils import Client, localhost, port
from client_student import client_sends_a_ping
import time


async def pingpong_client(ping, pong, loop):
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop)
    client = Client(reader, writer)

    while True:
        with ping:
            ping.wait()

        await client_sends_a_ping(client)
        data = await client.receive_message()
        if data == "Pong":
            time.sleep(1)
            with pong:
                pong.notifyAll()


def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = ClientBox(rt, lambda: print('Ping!'), ping, pong)
    rt.mainloop()


def start_asyncio():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pingpong_client(ping, pong, loop))
    loop.close()


if __name__ == "__main__":
    ping = Condition()
    pong = Condition()

    # Create and start gui
    start_gui(ping, pong)

    asyncio_worker = Thread(target=start_asyncio, daemon=True)
    asyncio_worker.start()
