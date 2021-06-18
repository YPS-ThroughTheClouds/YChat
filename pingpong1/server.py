import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import SocketHandler, MainServer, port, message_is_ping,Message


class Server(SocketHandler):
    # Specify what should occur when a server receives a message
    def handle_read(self):
        msg = self.receive_message()
        print(msg)
        if msg == Message.Ping: 
            self.send_message(Message.Pong)

# Sets up the TCP connection between the Server and the Client
server = MainServer(port, Server)

asyncore.loop()



