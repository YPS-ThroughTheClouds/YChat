import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import Client2Box
from utils2 import Client, localhost, port
from client2_student import client_sends_a_pong
import time


async def pingpong_client(ping, pong, loop):
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop)
    client = Client(reader, writer)

    while True:
        data = await client.receive_message()
        if data == "Ping":
            time.sleep(1)
            with ping:
                ping.notify()

            await client_sends_a_pong(client, data)


def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = Client2Box(rt, lambda: print('Ping!'), lambda: print('Pong!'), ping, pong)
    rt.mainloop()


def start_asyncio(loop):
    loop.run_until_complete(pingpong_client(ping, pong, loop))
    loop.close()


if __name__ == "__main__":
    ping = Condition()
    pong = Condition()

    loop = asyncio.get_event_loop()
    gui_worker = Thread(target=start_asyncio, args=(loop,), daemon=True)
    gui_worker.start()

    # Create and start message worker
    start_gui(ping, pong)
