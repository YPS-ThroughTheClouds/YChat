import enum
import asyncore
import socket

from server_student import server_sends_a_pong

port = 8888

class Client(asyncore.dispatcher_with_send):
    host = "localhost"

    def __init__(self, map=None):
        asyncore.dispatcher_with_send.__init__(self, map=map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, port))
        self.out_buffer = ''
        self.in_buffer = ''

    def handle_read(self):
        # Do something with data
        data = self.receive_message()
        print(data)

    def readable(self):
        #Test for select() and friends
        return True

    def handle_close(self):
        #Flush the buffer
        while self.writable():
            self.handle_write()
        self.close()
    
    def receive_message(self):
        receivedData = self.recv(8192)
        if receivedData == b'Ping':
            return "Ping"
        elif receivedData == b'Pong':
            return "Pong"
        else:
            return "Uknown message"

    def send_message(self, data):
        if data == "Ping":
            self.out_buffer = bytes('Ping', 'ascii')
        elif data == "Pong":
            self.out_buffer = bytes('Pong', 'ascii')
        else:
            print("Message was not a Ping or Pong type. Please try again.")


class MainServer(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('',port))
        self.listen(5)
        self.in_buffer = ''

    def handle_accept(self):
        newSocket, address = self.accept(  )
        print ("Connected from", address)
        SocketHandler(newSocket)

class SocketHandler(asyncore.dispatcher_with_send):
    def handle_close(self):
        self.close()
    
    def receive_message(self):
        receivedData = self.recv(8192)
        if receivedData == b'Ping':
            return "Ping"
        elif receivedData == b'Pong':
            return "Pong"
        else:
            return "Message Unknown"

    def send_message(self, data):
        if data == "Ping":
            self.send(b'Ping')
        elif data == "Pong":
            self.send(b'Pong')
        else:
            print("Message was not a Message type. Please try again.")
    
    def handle_read(self):
        msg = self.receive_message()
        print(msg)
        server_sends_a_pong(self, msg)
        

