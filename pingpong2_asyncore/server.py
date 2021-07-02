import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils2 import SocketHandler, MainServer, port, Message, get_other_client, sockets


class Server(SocketHandler):
    # Specify what should occur when the server receives a message
    def handle_read(self):
        msg = self.receive_message()
        if (msg == Message.Ping) | (msg == Message.Pong): 
            self.forward_message(msg)

# Sets up the TCP connection between the Server and the Clients
server = MainServer(port, Server)

asyncore.loop()



