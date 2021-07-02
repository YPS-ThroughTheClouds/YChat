import asyncore
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import MainServer, port
      
# Sets up the TCP connection between the Server and the Client
server = MainServer(port)

asyncore.loop()



