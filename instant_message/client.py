import asyncio 
import tkinter as tk
import time
from threading import Thread, Condition, Lock
from gui import ClientBox
from utils4 import Client, localhost, port
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

async def client_receiver(client):
    while True:
        # await asyncio.sleep(1)
        await client.receive_message()

async def client_sender(client, send_queue):
    while True:
        await asyncio.sleep(1)
        msg_type, msg_data = send_queue.get()

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


async def client(receive_queue, loop): 
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop) 
    client = Client(reader, writer, receive_queue)
    return client

def start_gui(send_queue, receive_queue):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = ClientBox(rt, send_queue, receive_queue)
    rt.mainloop()

if __name__ == "__main__":
    button_cv = Condition()
    completed_cv = Condition()
    mutex = Lock()
    flags = [False, False, False, False, False]
    send_queue = Queue()
    receive_queue = Queue()

    # Create and start message worker
    gui_worker = Thread(target=lambda: start_gui(send_queue, receive_queue), daemon=True)
    gui_worker.start()

    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(client(receive_queue, loop)) 

    loop.run_until_complete(asyncio.gather(
        client_sender(client, send_queue),
        client_receiver(client)
    ))

    loop.close()