import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import ServerBox
from utils2 import Server, localhost, port, sockets
from server_student import server_forwards_message
import time

global ping
global pong

async def pingpong_socket_handler(reader, writer):
    server = Server(reader, writer)
    sockets.append(server)

    while True: 
        msg = await server.receive_message()
        if msg == "Ping":
            with ping:
                ping.notify()
            time.sleep(1)
            await server_forwards_message(server, msg)
        
        if msg == "Pong":
            with pong:
                pong.notify()
            time.sleep(1)
            await server_forwards_message(server, msg)
            


def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    pong_wnd = ServerBox(rt, lambda: print('Forwarding Ping!'), lambda: print('Forwarding Pong!'), ping, pong)
    rt.mainloop()

if __name__ == "__main__":

    ping = Condition()
    pong = Condition()

    # Create and start gui worker
    gui_worker = Thread(target=lambda: start_gui(ping,pong), daemon=True)
    gui_worker.start()

    loop = asyncio.get_event_loop() 
    coro = asyncio.start_server(pingpong_socket_handler, localhost, port, loop=loop) 
    server = loop.run_until_complete(coro)
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