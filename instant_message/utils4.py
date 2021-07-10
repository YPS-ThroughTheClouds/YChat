
from collections import namedtuple
from queue import Queue

localhost = '127.0.0.1'
port = 8888
sockets = []

users = {}
active_users = {}
MessageData = namedtuple("MessageData", "type, data")

register_q = Queue()
login_q = Queue()
request_q = Queue()

class Client:
    def __init__(self, reader, writer, queue):
        self.reader = reader
        self.writer = writer
        self.queue = queue

    async def receive_message(self):
        data = await self.reader.read(8192)
        message = data.decode()
        receivedMessages = message.split(' EOM')
        print(receivedMessages)

        for message in receivedMessages:
            messages = message.split(',') 
            if messages[0] == "RegistrationSuccessful":
                self.queue.put((messages[0], ""))
            elif messages[0] == "RegistrationFailed":
                self.queue.put((messages[0], ""))
            elif messages[0] == "LoginSuccessful":
                self.queue.put((messages[0], ""))
            elif messages[0] == "LoginFailed":
                self.queue.put((messages[0], ""))
            elif messages[0] == "UserList":
                print("User list")
                i = 1
                msg = ""
                while i < len(messages):
                    msg += messages[i]
                    msg += ","
                    i += 1
                
                self.queue.put((messages[0], msg))
            elif messages[0] == "Msg":
                self.queue.put((messages[0], messages[1] + "," + messages[2]))
            else:
                print("unknown messages")

    async def send_message(self, data):
        self.writer.write((data + " EOM").encode())
        await self.writer.drain()
    
    async def register(self, username):
        out_buffer = "Register,"
        out_buffer += username
        await self.send_message(out_buffer)

    async def login(self, username):
        out_buffer = "Login,"
        out_buffer += username
        await self.send_message(out_buffer)

    async def request_registry(self):
        out_buffer = "RequestUsers"
        await self.send_message(out_buffer)


class Server:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    
    def get_addr_key(self):
        return self.writer.get_extra_info('peername')

    async def receive_message(self):
        data = await self.reader.read(8192)
        message = data.decode()
        receivedMessages = message.split(' EOM')
        print(receivedMessages)

        separated_messages = []

        for message in receivedMessages:
            messages = message.split(',') 
            if messages[0] == "Register":
                separated_messages.append(MessageData("Register", messages[1: len(messages)]))
            elif messages[0] == "Login":
                separated_messages.append(MessageData("Login", messages[1: len(messages)]))
            elif messages[0] == "RequestUsers":
                separated_messages.append(MessageData("RequestUsers", []))
            elif messages[0] == "CloseConnection":
                separated_messages.append(MessageData("CloseConnection", []))
            elif messages[0] == "Msg":
                separated_messages.append(MessageData("Msg", messages[1: len(messages)]))
            else:
                separated_messages.append(MessageData("Unknown", []))
        
        return separated_messages

    async def send_message(self, data):
        self.writer.write((data + " EOM").encode())
        await self.writer.drain()

    async def registration_successful(self, username):
        await self.send_message("RegistrationSuccessful")
        register_q.put("Registered client " + username)

    async def registration_failed(self, username):
        await self.send_message("RegistrationFailed")
        register_q.put("Failed to register client " + username)

    async def login_successful(self, username):
        await self.send_message("LoginSuccessful")
        login_q.put("client " + username + " logged in successfully")

    async def login_failed(self, username):
        await self.send_message("LoginFailed")
        login_q.put("Failed to login client " + username)
    
    async def request_denied(self):
        await self.send_message("RequestDenied")
        request_q.put("Denied request of client")
    
    async def send_registry(self):
        requesting_client = self.get_addr_key()
        msg = "UserList"
        for key in active_users:
            if key != requesting_client:
                msg += ","
                msg += active_users[key]
        
        await self.send_message(msg)
        request_q.put("Sent registry to client " + active_users[requesting_client])
    
    async def forward_message(self, user, msg):
        msg = "Msg," + active_users[self.get_addr_key()] + "," + msg 
        print("forwarding message: ", msg)
        recipient = get_client(user)
        await recipient.send_message(msg)

    def registered(self):
        if self.get_addr_key() in users:
            return True
        else:
            False

    def register_user(self, username):
        users[self.get_addr_key()] = username
    
    def username_matches_record(self, username):
        if self.registered():
            return username == users[self.get_addr_key()]
        else:
            return False

    def logged_in(self):
        if self.get_addr_key() in active_users:
            return True
        else:
            return False

    def log_in_client(self, username):
        active_users[self.get_addr_key()] = username
    
    def username_exists(self, username):
        for key in users:
            if users[key] == username:
                return True
        
        return False
    
    def get_username(self):
        return active_users[self.get_addr_key()]
    
    def user_is_logged_in(self, username):
        for key in active_users:
            if active_users[key] == username:
                return True
        
        return False
    
        
def get_client(username):
    for key in active_users:
        if active_users[key] == username:
            peername = key
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y.get_addr_key()]
    indexes = get_indexes(peername, sockets)
    return sockets[indexes[0]]