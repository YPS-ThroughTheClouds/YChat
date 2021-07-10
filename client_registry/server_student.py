# """
# Description:
# In this function, write the actions a server should perform when it receives a request to register a client. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the client has already registered or if the username is taken
# 2. If it has, then send a registration_failed message
# 3. If not, register the client and send a registration_successful message
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# username (string): the username the client wants to register with
# 
# """
async def register_client(server, username):
    # Hint: `await server.registration_succesful(username)` and `await server.registration_failed(username)` 
    # can be used to respond to a login request

    # Hint: server.registered() returns true if the client has already been registered
    # Hint: server.username_exists(username) returns true if the given username is taken
    # Hint: server.register_user(username) can be used to register a client
    
    # `*** start ***`  
    if server.registered(): 
        print("Client is already registered")
        await server.registration_failed(username)
    elif server.username_exists(username):
        print("Username Exists")
        await server.registration_failed(username)      
    else:
        print("Adding user ", username)
        server.register_user(username)
        await server.registration_successful(username)

    # `*** end ***`  
        

# """
# Description:
# In this function, write the actions a server should perform when it receives a request to login a client. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the client has already registered and its username matches what the server has on record
# 2. If it has, login the client and send a login_successful message
# 3. If not, then send a login_failed message 
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# username (string): the username the client wants to login with
# 
# """
async def login_client(server, username):
    # Hint: `await server.login_succesful(username)` and `await server.login_failed(username)` 
    # can be used to respond to a login request

    # Hint: server.registered() returns true if the client has already been registered
    # Hint: server.username_matches_record(username) returns true if the given username matches the registered one
    # Hint: server.log_in_client(username) can be used to log in a client
    
    # `*** start ***`  

    if server.registered() & server.username_matches_record(username):
        print("Logging in client")
        server.log_in_client(username)
        await server.login_successful(username)
    else:
        print("Login failed")
        await server.login_failed(username)

    # `*** end ***`  

# """
# Description:
# In this function, write the actions a server should perform when it receives a request to send the client registry 
#
# To Do:
# You should complete the following steps:
# 1. Check if the client has already logged in
# 2. If it has, then send the registry
# 3. If not, send a request denied message
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# 
# """
async def send_registry_to_client(server):
    # Hint: `await server.send_registry()` and `await server.request_denied()` 
    # can be used to respond to a registry request

    # Hint: server.logged_in() returns true if the client has already logged in

    # `*** start ***`  

    if server.logged_in():
        print("Sending registry to client")
        await server.send_registry()
    else:
        print("Request denied")
        await server.request_denied()
        
    # `*** end ***`  

