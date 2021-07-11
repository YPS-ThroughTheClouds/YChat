import asyncio
import tkinter as tk
from threading import Thread, Condition
from queue import Queue
import queue
from gui import Client1Box
from utils2 import Client, localhost, port
from client_student import client_sends_a_ping
import time

async def client_receiver(client, pong):
    while True:
        msg = await client.receive_message()
        if msg == "Pong":
            time.sleep(0.75)
            with pong:
                pong.notify()


async def client_sender(client, ping_queue):
    while True:
        await asyncio.sleep(0.1)
        try:
            msg = ping_queue.get(False)
        except queue.Empty:
            msg = None
        
        if msg:
            await client_sends_a_ping(client)
        

async def create_client(loop):
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop)
    client = Client(reader, writer)
    return client

def start_gui(ping_cv, pong_queue):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = Client1Box(rt, lambda: print('Ping!'), lambda: print('Pong!'), ping_cv, pong_queue)
    rt.mainloop()


def start_asyncio(loop, ping_cv, pong_queue):
    client = loop.run_until_complete(create_client(loop))

    loop.run_until_complete(asyncio.gather(
        client_sender(client, pong_queue),
        client_receiver(client, ping_cv), 
        loop=loop
    ))

    loop.close()



if __name__ == "__main__":
    pong_cv = Condition()
    ping_queue = Queue()

    loop = asyncio.get_event_loop()
    gui_worker = Thread(target=start_asyncio, args=(loop,pong_cv, ping_queue), daemon=True)
    gui_worker.start()

    # Create and start message worker
    start_gui(pong_cv, ping_queue)
