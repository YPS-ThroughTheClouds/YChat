import asyncio
import tkinter as tk
from threading import Thread, Condition
from gui import PongBox
from utils import Server
from server_student import server_sends_a_pong 

global ping
global pong

async def handle_echo(reader, writer):
    server = Server(reader, writer)

    while True: 
        msg = await server.receive_message()

        if msg == "Ping":
            with ping:
                ping.notifyAll()

        await server_sends_a_pong(server, msg)


ping = Condition()
pong = Condition()

def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    pong_wnd = PongBox(rt, lambda: print('Pong!'), ping, pong)
    rt.mainloop()

# Create and start message worker
pong_worker = Thread(target=lambda: start_gui(ping,pong), daemon=True)
pong_worker.start()

loop = asyncio.get_event_loop() 
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop) 

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