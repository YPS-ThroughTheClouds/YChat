import asyncio
import time
import tkinter as tk
from queue import Queue
from threading import Thread, Condition

from client_student import client_sends_a_ping
from gui import ClientBox
from utils import Client, localhost, remotehost, port


async def pingpong_client(ping, pong, server_queue, start_cv, loop):
    msg = server_queue.get()
    if msg == "Local":
        host = localhost
    elif msg == "Remote":
        host = remotehost
    else:
        print("Error: This should never occur")

    with start_cv:
        start_cv.notify()

    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    client = Client(reader, writer)

    while True:
        with ping:
            ping.wait()

        await client_sends_a_ping(client)
        data = await client.receive_message()
        if data == "Pong":
            time.sleep(0.75)
            with pong:
                pong.notifyAll()


def start_gui(ping, pong, server_queue, start_cv):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = ClientBox(rt, lambda: print('Ping!'), ping, pong, server_queue, start_cv)
    rt.mainloop()


def start_asyncio(ping, pong, server_queue, start_cv, loop):
    loop.run_until_complete(pingpong_client(ping, pong, server_queue, start_cv, loop))
    loop.close()


if __name__ == "__main__":
    ping = Condition()
    pong = Condition()
    server_queue = Queue()
    start_cv = Condition()

    loop = asyncio.get_event_loop()
    asyncio_worker = Thread(target=start_asyncio, args=(ping, pong, server_queue, start_cv, loop,), daemon=True)
    asyncio_worker.start()

    # Create and start gui
    start_gui(ping, pong, server_queue, start_cv)
