import enum

def server_forward_message(sender, receiver, message_type):
    print 'sending message'

def server_recv_message():
    print 'receiving message'

def client_send_message(sender, receiver, message_type):
    print 'sending message'

def client_recv_message():
    print 'receiving message'

class MessageType(enum.Enum):
    Ping 
    Pong 

def init_server():
    print 'initializing server'

def init_client1():
    print 'initializing client1'

def init_client2():
    print 'initializing client2'