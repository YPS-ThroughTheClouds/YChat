import enum
import asyncore
import socket

port = 8889
sockets = []

class Message(enum.Enum):
    Ping = 0
    Pong = 1
    Unknown = 2

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
        if receivedData == "Ping":
            return Message.Ping
        elif receivedData == "Pong":
            return Message.Pong
        else:
            return Message.Unknown

    def send_message(self, data):
        if data == Message.Ping:
            self.out_buffer += "Ping"
        elif data == Message.Pong:
            self.out_buffer += "Pong"
        else:
            print("Message was not a Message type. Please try again.")


class MainServer(asyncore.dispatcher):
    def __init__(self, port, handler):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('',port))
        self.listen(5)
        self.in_buffer = ''
        self.handler = handler

    def handle_accept(self):
        newSocket, address = self.accept(  )
        print ("Connected from", address)
        sockets.append(self.handler(newSocket))


class SocketHandler(asyncore.dispatcher_with_send):
    def handle_close(self):
        print("Disconnected from", self.getpeername())
        remove_from_socket_list(self.getpeername())
        self.close()
    
    def receive_message(self):
        receivedData = self.recv(8192)
        if receivedData == "Ping":
            return Message.Ping
        elif receivedData == "Pong":
            return Message.Pong
        else:
            return Message.Unknown

    def send_message(self, data):
        if data == Message.Ping:
            self.send("Ping")
        elif data == Message.Pong:
            self.send("Pong")
        else:
            print("Message was not a Message type. Please try again.")
    
    def forward_message(self, msg):
        index = get_other_client(self.getpeername())
        if len(index) != 0: 
            sockets[index[0]].send_message(msg)


def get_other_client(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x != y.getpeername()]
    indexes = get_indexes(peername, sockets)
    return indexes

def remove_from_socket_list(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y.getpeername()]
    del sockets[get_indexes(peername, sockets)[0]]
