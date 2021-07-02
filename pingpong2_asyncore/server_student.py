import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils2 import SocketHandler, MainServer, port, Message, get_other_client, sockets


class Server(SocketHandler):
    # Specify what should occur when a server receives a message
    def handle_read(self):
        msg = self.receive_message()
        
        # *** start ***
        # Forward Ping and Pong message to other client
        # *** end ***


# Sets up the TCP connection between the Server and the Client
server = MainServer(port, Server)

asyncore.loop()



