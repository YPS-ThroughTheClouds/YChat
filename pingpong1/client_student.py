import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import Client, Message

# Sets up the connection between ther server and the client
client = Client()

# *** start ***
# Send a Ping message
# *** end ***

asyncore.loop()



