import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import Client
from client_student import client_sends_a_ping

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client = Client()

# Send a packet over the TCP connection
client_sends_a_ping(client)

asyncore.loop()




