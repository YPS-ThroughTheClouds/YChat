import asyncio
import tkinter as tk
import queue
from queue import Queue
from threading import Thread, Condition, Lock

from gui import ClientBox
from utils4 import Client, localhost, remotehost, host, port


async def client_receiver(client):
    while True:
        # await asyncio.sleep(1)
        await client.receive_message()


async def client_sender(client, send_queue):
    while True:
        await asyncio.sleep(1)
        try:
            msg_type, msg_data = send_queue.get(False)
        except queue.Empty:
            msg_type = None


        if msg_type:
            if msg_type == "Register":
                username = msg_data
                await register_user(client, username)

            elif msg_type == "Login":
                username = msg_data
                await login(client, username)

            elif msg_type == "Request":
                await request_user_list(client)

            elif msg_type == "Msg":
                await client.send_message("Msg," + msg_data)

            elif msg_type == "CloseConnection":
                await client.send_message("CloseConnection")

async def register_user(client, username):
    await client.register(username)


async def login(client, username):
    await client.login(username)


async def request_user_list(client):
    await client.request_registry()


async def create_client(receive_queue, server_queue, start_cv, loop):
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
    client = Client(reader, writer, receive_queue)
    return client


def start_gui(send_queue, receive_queue, server_queue, start_cv):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = ClientBox(rt, send_queue, receive_queue, server_queue, start_cv)
    rt.mainloop()


def start_asyncio(loop, send_queue, receive_queue, server_queue, start_cv):
    client = loop.run_until_complete(create_client(receive_queue, server_queue, start_cv, loop))

    loop.run_until_complete(asyncio.gather(
        client_sender(client, send_queue),
        client_receiver(client), loop=loop
    ))

    loop.close()


if __name__ == "__main__":
    button_cv = Condition()
    completed_cv = Condition()
    mutex = Lock()
    flags = [False, False, False, False, False]
    send_queue = Queue()
    receive_queue = Queue()
    server_queue = Queue() 
    start_cv = Condition()

    # Create and start message worker
    loop = asyncio.get_event_loop()
    asyncio_worker = Thread(target=start_asyncio, args=(loop, send_queue, receive_queue, server_queue, start_cv), daemon=True)
    asyncio_worker.start()

    start_gui(send_queue, receive_queue, server_queue, start_cv)
