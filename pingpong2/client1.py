import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils2 import Client, Message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client = Client()

# Send a packet over the TCP connection
client.send_message(Message.Ping)

asyncore.loop()




