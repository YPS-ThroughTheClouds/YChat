from utils3 import Server, users, active_users
# """
# Description:
# In this function, write the actions a server should perform when it receives a message. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the received message is a "Ping" or a "Pong"
# 2. If so, forward the message to the other client
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# msg (string): the message the server has just received from a client
# 
# """
async def server_forwards_message(server, msg):
    # `*** start ***`  
    
    # Hint: You can send forward a message using the `await server.forward_message(msg)` function.
    if (msg == "Ping") | (msg == "Pong"):
        await server.forward_message(msg)
    
    # `*** end ***`  

async def register_client(server, username):
    addr = server.get_addr_key()
    print(addr)
    if addr in users:
        print("Client is already registered")
        await server.registration_failed(username)
    else:
        print("Adding user ", username)
        users[addr] = username
        await server.registration_successful(username)

async def login_client(server, username):
    addr = server.get_addr_key()

    if (addr in users) & (username == users[addr]):
        print("Logging in client")
        active_users[addr] = username
        await server.login_successful(username)
    else:
        print("Login failed")
        await server.login_failed(username)

async def send_registry_to_client(server):
    addr = server.get_addr_key()

    if addr in active_users:
        print("Sending registry to client")
        username = active_users[addr]
        await server.send_registry(username)
    else:
        print("Request denied")
        await server.request_denied()
