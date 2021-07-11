import asyncio
import time
import tkinter as tk
from threading import Thread, Condition

from gui import ServerBox
from server_student import register_client, login_client, send_registry_to_client
from utils3 import Server, localhost, port, sockets, active_users

global register
global login
global request_users


async def socket_handler(reader, writer):
    server = Server(reader, writer)
    sockets.append(server)

    while True:
        msgs = await server.receive_message()
        for msg in msgs:
            time.sleep(0.5)
            if msg.type == 'Register':
                await register_client(server, msg.data[0])
                with register:
                    register.notify()
            if msg.type == "Login":
                await login_client(server, msg.data[0])
                with login:
                    login.notify()
            if msg.type == "RequestUsers":
                await send_registry_to_client(server)
                with request_users:
                    request_users.notify()

            if msg.type == "CloseConnection":
                sockets.remove(server)
                addr = server.get_addr_key()
                if addr in active_users:
                    del active_users[addr]


def start_gui(register, login, request_users):
    rt = tk.Tk()
    rt.withdraw()
    pong_wnd = ServerBox(rt, register, login, request_users)
    rt.mainloop()


def start_asyncio(loop):
    core = asyncio.start_server(socket_handler, localhost, port, loop=loop)
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
    register = Condition()
    login = Condition()
    request_users = Condition()

    # Create and start gui worker
    loop = asyncio.get_event_loop()
    asyncio_worker = Thread(target=start_asyncio, args=(loop,), daemon=True)
    asyncio_worker.start()

    start_gui(register, login, request_users)
