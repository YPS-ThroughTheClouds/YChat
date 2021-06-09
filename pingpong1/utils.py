import enum

def send_message(message_type):
    print 'sending message'

def recv_message():
    print 'receiving message'

class MessageType(enum.Enum):
    Ping 
    Pong 

def init_server():
    print 'initializing server'

def init_client():
    print 'initializing client'