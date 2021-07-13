from utils import users, active_users

# Hint: `users` is the dictionary of registered users.
# Hint: `active_users` is the dictionary of logged in users.


# """
# Description:
# Returns true if the client has already been registered. 
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# username (string): the username the client wants to register with.
# 
# """
def registered(key, username):
    # `*** start ***`

    return key in users

    # `*** end ***`  

# """
# Description:
# Returns true if the given username is taken.
#
# Parameters:
# username (string): the username the client wants to register with.
# 
# """
def username_exists(username): 
    # `*** start ***`

    for key in users:
        if users[key] == username:
            return True
    return False

    # `*** end ***`  

# """
# Description:
# This function registers a client by adding them to `users` list.
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
# Hint: It is your responsibility to make sure another user with the same username is not already registered.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# username (string): the username the client wants to register with.
# 
# """
def register_user(key, username):  
    # `*** start ***`

    users[key] = username

    # `*** end ***`  

# """
# Description:
# Returns true if the given username matches the registered one.  
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# username (string): the username the client wants to register with.
# 
# """
def username_matches_record(key, username):
    # `*** start ***`

    if registered(key, username):
        return username == users[key]
    else:
        return False

    # `*** end ***`  

# """
# Description:
# This function logs in a client by adding them to `active_users` list.
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
# Hint: It is your responsibility to make sure the user is already registered when calling this function.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# username (string): the username the client wants to register with.
# 
# """ 
def log_in_client(key, username):
    # `*** start ***`

    active_users[key] = username

    # `*** end ***`  

# """
# Description:
# Returns true if the client has already logged in.
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# username (string): the username the client wants to register with.
# 
# """ 
def logged_in(key, username):
    # `*** start ***`

    return key in active_users

    # `*** end ***`  

# """
# Description:
# Returns the username of a client.
#
# Hint: Each client's key can be retrieved using the `server.get_addr_key()` function.
# Hint: It is your responsibility to make sure the user is already registered when calling this function.
#
# Parameters:
# key (string): the client's unqiue key used to index into the dictionary.  
# 
# """ 
def get_username(key):
    # `*** start ***`

    return users[key]

    # `*** end ***`  


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

    # `*** start ***`

    key = server.get_addr_key()  
    if registered(key, username):
        print("Client is already registered")
        await server.registration_failed(username)
    elif username_exists(username):
        print("Username Exists")
        await server.registration_failed(username)
    else:
        print("Adding user ", username)
        register_user(key, username)
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

    # `*** start ***`  

    key = server.get_addr_key()  
    if registered(key, username) & username_matches_record(key, username):
        print("Logging in client")
        log_in_client(key, username)
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

    # `*** start ***`  

    key = server.get_addr_key() 
    username = get_username(key) 
    if logged_in(key, username):
        print("Sending registry to client")
        await server.send_registry()
    else:
        print("Request denied")
        await server.request_denied()

    # `*** end ***`
