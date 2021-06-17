#!/usr/bin/env python

# This script opens CONNECTIONS simultaneous connections to a remote socket,
# and sends a fixed string before closing the connection. The process is then
# repeated indefinitely

# Intended to unit test the tcp_server.py script

import asyncore
import socket
import time



class Client(asyncore.dispatcher_with_send):
    host = "localhost"
    port = 8881
    mesg = "Hello World\n"

    def __init__(self, map=None):
        asyncore.dispatcher_with_send.__init__(self, map=map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))
        self.out_buffer = ''
        self.in_buffer = '' 

    def handle_read(self):
        # Do something with data
        data = self.recv(4096)
        # self.in_buffer += data
        print data

    # def handle_write(self):
    #     #Data must be placed in a buffer somewhere.
    #     #(In this case out_buffer)
    #     sent = self.send(self.out_buffer)
    #     self.out_buffer = self.out_buffer[sent:]

    def readable(self):
        #Test for select() and friends
        return True

    # #There is no 'e' in 'writeable' here.
    # def writable(self):
    #     #Test for select(). Must have data to write
    #     #otherwise select() will trigger
    #     if self.connected and len(self.out_buffer) > 0:
    #         return True
    #     return False

    def handle_close(self):
        #Flush the buffer
        while self.writable():
            self.handle_write()
        self.close()

    def write_data(self, data):
        self.out_buffer += data

client = Client()
client.write_data("hello")
asyncore.loop()
