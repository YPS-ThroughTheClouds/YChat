import asyncio 
import tkinter as tk
from threading import Thread, Condition
from gui import PingBox

async def tcp_echo_client(ping, pong, loop): 
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop) 
    
    while True:
        with ping:
            ping.wait()
    
        writer.write("Ping".encode())

        data = await reader.read(100)
        print(data.decode())
        if data.decode() == "Pong":
            with pong:
                pong.notifyAll()
        # print('Close the socket') 
        # writer.close() 


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