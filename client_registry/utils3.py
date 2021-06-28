import enum
import asyncore
import socket
from collections import namedtuple

port = 8889
sockets = []
users = {}
active_users = {}

class Message(enum.Enum):
    Ping = 0
    Pong = 1
    Register = 2
    RegistrationComplete = 3
    Login = 4
    LoginComplete = 5
    RequestUsers = 6
    UserList = 7
    Unknown = 8

MessageData = namedtuple("MessageData", "type, data")

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
        receivedMessages = receivedData.split(' ')
        print(receivedMessages)

        separated_messages = []

        for message in receivedMessages:
            messages = message.split(',') 
            if messages[0] == "Ping":
                separated_messages.append(MessageData(Message.Ping, []))
            elif messages[0] == "Pong":
                separated_messages.append(MessageData(Message.Pong, []))
            elif messages[0] == "RegistrationComplete":
                separated_messages.append(MessageData(Message.RegistrationComplete, []))
            elif messages[0] == "LoginComplete":
                separated_messages.append(MessageData(Message.LoginComplete, []))
            elif messages[0] == "UserList":
                separated_messages.append(MessageData(Message.UserList, []))
            else:
                return separated_messages.append(MessageData(Message.Unknown, []))
        
        return separated_messages

    def send_message(self, data):
        if data == Message.Ping:
            self.out_buffer += "Ping "
        elif data == Message.Pong:
            self.out_buffer += "Pong "
        elif data == Message.Register:
            self.out_buffer += "Register "
        elif data == Message.Login:
            self.out_buffer += "Login "
        elif data == Message.RequestUsers:
            self.out_buffer += "RequestUsers "
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
        receivedMessages = receivedData.split(' ')
        print(receivedMessages)

        separated_messages = []

        for message in receivedMessages:
            messages = message.split(',') 
            if messages[0] == "Ping":
                separated_messages.append(MessageData(Message.Ping, []))
            elif messages[0] == "Pong":
                separated_messages.append(MessageData(Message.Pong, []))
            elif messages[0] == "Register":
                separated_messages.append(MessageData(Message.Register, messages[1: len(messages)]))
            elif messages[0] == "Login":
                separated_messages.append(MessageData(Message.Login, messages[1: len(messages)]))
            elif messages[0] == "RequestUsers":
                separated_messages.append(MessageData(Message.RequestUsers, []))
            else:
                separated_messages.append(MessageData(Message.Unknown, []))
        
        return separated_messages

    def send_message(self, data):
        if data == Message.Ping:
            self.send("Ping ")
        elif data == Message.Pong:
            self.send("Pong ")
        elif data == Message.RegistrationComplete:
            self.send("RegistrationComplete ")
        elif data == Message.LoginComplete:
            self.send("LoginComplete ")
        elif data == Message.UserList:
            #ToDo: need to send whole dictionary
            self.send("UserList ")
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
