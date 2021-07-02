import asyncore
import sys
import os
from threading import Thread, Condition
import tkinter as tk
from gui import PingBox

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import Client
from client_student import client_sends_a_ping

def client_loop(client):
    while True:
        # with client.ping:
        #     client.ping.wait()
        client_sends_a_ping(client)



ping = Condition()
pong = Condition()

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client = Client(ping, pong)

def start_gui(ping, pong):
    rt = tk.Tk()
    rt.withdraw()
    ping_wnd = PingBox(rt, lambda: print('Ping!'), ping, pong)
    rt.mainloop()


# Create and start message worker
pong_worker = Thread(target=lambda: start_gui(ping, pong), daemon=True)
pong_worker.start()

# Create and start message worker
client_worker = Thread(target=lambda: client_loop(client), daemon=True)
client_worker.start()

asyncore.loop()




