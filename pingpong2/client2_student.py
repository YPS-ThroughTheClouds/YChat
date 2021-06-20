import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils2 import Client, Message

class Client2(Client):
    def handle_read(self):
        msg = self.receive_message()
        print(msg)

        # *** start ***
        # Send Pong message in response to a Ping
        # *** end ***
            


# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client = Client2()

asyncore.loop()




