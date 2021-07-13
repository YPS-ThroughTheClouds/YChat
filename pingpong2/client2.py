import asyncio
import tkinter as tk
from threading import Thread, Condition
from queue import Queue
import queue
from gui import Client2Box
from utils import Client, localhost, remotehost, host, port
from client_logic import client2_logic
import time


async def client_receiver(client, ping):
    while True:
        msg = await client.receive_message()
        if msg == "Ping":
            time.sleep(0.75)
            with ping:
                ping.notify()


async def client_sender(client, pong_queue):
    while True:
        await asyncio.sleep(0.1)
        try:
            msg = pong_queue.get(False)
        except queue.Empty:
            msg = None

        if msg:
            await client2_logic(client)


async def create_client(loop, start_cv, server_queue):
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
    return client


def start_gui(ping_cv, pong_queue, start_cv, server_queue):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = Client2Box(rt, lambda: print('Ping!'), lambda: print('Pong!'), ping_cv, pong_queue, start_cv,
                          server_queue)
    rt.mainloop()


def start_asyncio(loop, ping_cv, pong_queue, start_cv, server_queue):
    client = loop.run_until_complete(create_client(loop, start_cv, server_queue))

    loop.run_until_complete(asyncio.gather(
        client_sender(client, pong_queue),
        client_receiver(client, ping_cv),
        loop=loop
    ))

    loop.close()


if __name__ == "__main__":
    ping_cv = Condition()
    pong_queue = Queue()
    start_cv = Condition()
    server_queue = Queue()

    loop = asyncio.get_event_loop()
    gui_worker = Thread(target=start_asyncio, args=(loop, ping_cv, pong_queue, start_cv, server_queue), daemon=True)
    gui_worker.start()

    # Create and start message worker
    start_gui(ping_cv, pong_queue, start_cv, server_queue)
