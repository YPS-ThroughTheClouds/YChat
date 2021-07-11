import asyncio
import tkinter as tk
from queue import Queue
from threading import Thread, Condition, Lock
from client_student import register_user, login, request_user_list
from gui import ClientBox
from utils3 import Client, localhost, port


async def client(button_cv, completed_cv, mutex, flags, send_queue, receive_queue, loop):
    reader, writer = await asyncio.open_connection(localhost, port, loop=loop)
    client = Client(reader, writer, receive_queue)

    while True:
        with button_cv:
            button_cv.wait()

        mutex.acquire()

        if flags[0]:  # Register
            username = send_queue.get()
            await register_user(client, username)
            await client.receive_message()
            flags[0] = False

        elif flags[1]:  # Login
            username = send_queue.get()
            await login(client, username)
            await client.receive_message()
            flags[1] = False

        elif flags[2]:  # Request
            await request_user_list(client)
            await client.receive_message()
            flags[2] = False

        else:  # Close connection
            await client.send_message("CloseConnection ")

        mutex.release()

        with completed_cv:
            completed_cv.notify()


def start_gui(button_cv, completed_cv, mutex, flags, send_queue, receive_queue):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = ClientBox(rt, button_cv, completed_cv, mutex, flags, send_queue, receive_queue)
    rt.mainloop()


def start_asyncio(loop):
    loop.run_until_complete(client(button_cv, completed_cv, mutex, flags, send_queue, receive_queue, loop))
    loop.close()


if __name__ == "__main__":
    button_cv = Condition()
    completed_cv = Condition()
    mutex = Lock()
    flags = [False, False, False]
    send_queue = Queue()
    receive_queue = Queue()

    loop = asyncio.get_event_loop()
    asyncio_worker = Thread(target=start_asyncio, args=(loop,), daemon=True)
    asyncio_worker.start()

    # Create and start gui
    start_gui(button_cv, completed_cv, mutex, flags, send_queue, receive_queue)

