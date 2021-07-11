import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import Client1Box
from utils2 import Client, localhost, port
import time


async def pingpong_client(ping, pong, loop):
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop)
    client = Client(reader, writer)

    while True:
        with ping:
            ping.wait()

        await client.send_message("Ping")

        msg = await client.receive_message()
        if msg == "Pong":
            time.sleep(1)
            with pong:
                pong.notify()


def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = Client1Box(rt, lambda: print('Ping!'), lambda: print('Pong!'), ping, pong)
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
