import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils3 import SocketHandler, MainServer, port, Message, get_other_client, sockets, users


class Server(SocketHandler):
    # Specify what should occur when the server receives a message
    def handle_read(self):
        msgs = self.receive_message()
        for msg in msgs:
            if msg.type == Message.Register:
                print("Registering user: ", self.getpeername())
                self.send_message(Message.RegistrationComplete)
            elif msg.type == Message.Login:
                print("Logging in user: ", self.getpeername())
                self.send_message(Message.LoginComplete)
            elif msg.type == Message.RequestUsers:
                print("Sending user list to user: ", self.getpeername())
                self.send_message(Message.UserList)
            else:
                print("No other message supported by this server")

# Sets up the TCP connection between the Server and the Clients
server = MainServer(port, Server)

asyncore.loop()



