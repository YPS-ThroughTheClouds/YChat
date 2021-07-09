# """
# Description:
# In this function, write the actions a server should perform when it receives a request to register a client. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the client has already registered 
# (Hint: server.registered() returns true if the client has already been registered)
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

    if server.registered():
        # `*** start ***`  

        # `*** end ***`  

    else:
        # `*** start ***`  
        # Hint: You can register a client using the `server.register_user(username)` function

        # `*** end ***`  
        

# """
# Description:
# In this function, write the actions a server should perform when it receives a request to login a client. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the client has already registered and its username matches what the server has on record
# (Hint: server.registered() returns true if the client has already been registered)
# 2. If it has, then send a login_failed message
# 3. If not, login the client and send a login_successful message
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# username (string): the username the client wants to login with
# 
# """
async def login_client(server, username):
    # Hint: `await server.login_succesful(username)` and `await server.login_failed(username)` 
    # can be used to respond to a login request

    if server.registered() & server.username_matches_record(username):
        # `*** start ***`  
        # Hint: You can login a client using the `server.log_in_client(username)` function

        # `*** end ***`  
    else:
        # `*** start ***`  

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

    if server.logged_in():
        # `*** start ***`  

        # `*** end ***`  
    else:
        # `*** start ***`  
        
        # `*** end ***`  

