import enum

class MessageType(enum.Enum):
    Ping 
    Pong 


class Server:
    def init():
        print 'initializing server'

    def send_message(message_type):
        print 'sending message'
    
    def recv_message():
        print 'receiving message'

class Client:
    def init():
        print 'initializing client'
    
    def send_message(message_type):
        print 'sending message'

    def recv_message():
        print 'receiving message'