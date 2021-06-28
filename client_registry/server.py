import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils3 import SocketHandler, MainServer, port, Message, get_other_client, sockets, users, active_users


class Server(SocketHandler):
    # Specify what should occur when the server receives a message
    def handle_read(self):
        msgs = self.receive_message()
        for msg in msgs:
            if msg.type == Message.Register:
                print("Registering user: ", self.getpeername(), "with username: ", msg.data[0])
                users[self.getpeername()] = msg.data[0]
                self.send_message(Message.RegistrationComplete)

            elif msg.type == Message.Login:
                if users[self.getpeername()] == msg.data[0]:
                    print("User ", msg.data[0], " is registered. Logging in ...")
                    active_users[self.getpeername()] = msg.data[0]
                    self.send_message(Message.LoginComplete)
                else:
                    print("User ", msg.data[0], " is not registered.")
                    self.send_message(Message.LoginFailed)

            elif msg.type == Message.RequestUsers:
                print("Sending user list to user: ", self.getpeername())
                self.send_user_list(self.getpeername())

            else:
                print("No other message supported by this server")

# Sets up the TCP connection between the Server and the Clients
server = MainServer(port, Server)

asyncore.loop()



