import asyncio 
import tkinter as tk
from threading import Thread, Condition
from gui import PongBox

global ping
global pong

async def handle_echo(reader, writer):

    while True: 
        data = await reader.read(100) 
        message = data.decode() 
        addr = writer.get_extra_info('peername') 
        print("Received %r from %r" % (message, addr))

        if message == "Ping":
            with ping:
                ping.notifyAll()

            with pong:
                pong.wait()
                writer.write("Pong".encode()) 
                await writer.drain() 

    # print("Close the client socket") 
    # writer.close() 

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