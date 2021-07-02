import enum
import asyncore
import socket
from collections import namedtuple

port = 8887
sockets = []
users = {}
active_users = {}

class Message(enum.Enum):
    Ping = 0
    Pong = 1
    Register = 2
    RegistrationComplete = 3
    RegsitrationFailed = 4
    Login = 5
    LoginComplete = 6
    LoginFailed = 7
    RequestUsers = 8
    UserList = 9
    Unknown = 10

MessageData = namedtuple("MessageData", "type, data")

class Client(asyncore.dispatcher_with_send):
    host = "localhost"
    user_list = []

    def __init__(self, map=None):
        asyncore.dispatcher_with_send.__init__(self, map=map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, port))
        self.out_buffer = ''
        self.in_buffer = ''

    def handle_read(self):
        # Do something with data
        messages = self.receive_message()
        if messages:
            for msg in messages:
                print(msg)
                if msg.type == Message.UserList:
                    self.user_list = msg.data

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
            elif messages[0] == "RegistrationFailed":
                separated_messages.append(MessageData(Message.RegistrationFailed, []))
            elif messages[0] == "LoginComplete":
                separated_messages.append(MessageData(Message.LoginComplete, []))
            elif messages[0] == "LoginFailed":
                separated_messages.append(MessageData(Message.LoginFailed, []))
            elif messages[0] == "UserList":
                separated_messages.append(MessageData(Message.UserList, {}))
            else:
                return separated_messages.append(MessageData(Message.Unknown, []))
        
        return separated_messages

    def send_message(self, data):
        if data == Message.Ping:
            self.out_buffer += "Ping "
        elif data == Message.Pong:
            self.out_buffer += "Pong "
        else:
            print("Message ", data, " not supported with this function")
        
    def register_user(self, username):
        self.out_buffer += "Register,"
        self.out_buffer += username
        self.out_buffer += " "
    
    def login(self, username):
        self.out_buffer += "Login,"
        self.out_buffer += username
        self.out_buffer += " "
    
    def request_user_list(self):
        self.out_buffer += "RequestUsers "

    def print_user_list(self):
        print(self.user_list)


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
        else:
            print("Message ", data, " not supported in this function.")
    
    def forward_message(self, msg):
        index = get_other_client(self.getpeername())
        if len(index) != 0: 
            sockets[index[0]].send_message(msg)
    
    def send_user_list(self, requesting_client):
        msg = "UserList"
        for key in active_users:
            if key != requesting_client:
                msg += ","
                msg += active_users[key]
        msg += " "
        self.send(msg)



def get_other_client(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x != y.getpeername()]
    indexes = get_indexes(peername, sockets)
    return indexes

def remove_from_socket_list(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y.getpeername()]
    del sockets[get_indexes(peername, sockets)[0]]
