import asyncio 
import tkinter as tk
from threading import Thread, Condition
from gui import PingBox
from utils import Client
from client_student import client_sends_a_ping

async def tcp_echo_client(ping, pong, loop): 
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop) 
    client = Client(reader, writer)

    while True:
        with ping:
            ping.wait()
    
        await client_sends_a_ping(client)

        data = await client.receive_message()

        if data == "Pong":
            with pong:
                pong.notifyAll()


ping = Condition()
pong = Condition()

def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = PingBox(rt, lambda: print('Ping!'), ping, pong)
    rt.mainloop()

# Create and start message worker
pong_worker = Thread(target=lambda: start_gui(ping,pong), daemon=True)
pong_worker.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(ping, pong, loop)) 
loop.close()