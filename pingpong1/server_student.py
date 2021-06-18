import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import SocketHandler, MainServer, port, message_is_ping,Message


class Server(SocketHandler):
    # function which specifies what should occur when a server receives a message
    def handle_read(self):
        msg = self.receive_message()
        print(msg)
        
        # *** start ***
        # check if message is a Ping, and respond with a Pong
        # *** end ***

# Sets up the connection between the Server and the Client
server = MainServer(port, Server)

asyncore.loop()



