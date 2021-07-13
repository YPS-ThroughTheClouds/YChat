# Client Registry Application

## Objective
In this application, we run multiple client programs and one server program in which the following steps should occur:
1. Each client registers a username with the server.
2. Each client logs in to the server.
3. Each client requests the client registry from the server

## Software Interface
You are provided skeleton code, with portions you must fill in yourself. The portions you must fill are demarcated by these comments:  
`*** start ***`  
`*** end ***`  

For the Server, we provide the following functions to send messages:  
`await registration_successful(self, username)`
`await registration_failed(self, username)`
`await login_successful(self, username)`
`await login_failed(self, username)`
`await request_denied(self)`
`await send_registry(self)`

For the client, we provide the following functions to send messages:  
`await register(self, username)`
`await login(self, username)`
`await request_registry(self)`

Under the hood, all of these functions call `await send_message(self, msg)`, but we have provided these helper methods so that you do not have to worry about creating the messages in the proper format.  

The registry on the server's side which stores the registered and logged in clients is implemented using Python dictionaries. 
Registered clients are stored in the global `users` variable. Logged in clients are stored in the global `active_users` variable.
The key value for both the dictionaries is a string containing the the clients IP address and socket number which is unique for each client.
The server can access the key value for each client by calling the server function:
`get_addr_key(self)`

The returned value is used to index into both the `users` and `active_users` dictionaries.
Remember, a client has to be registered with a unique username, and once it is registered it is never removed from the `users` list.
It is added and removed from the `active_users` list depending on if it is logged in.
The server will automatically log a user off if you close a client's window.

In addition to responding to client's requests, you must also implement functions that complete different server tasks such as adding clients to the registry and logging them in. You can use the following link (as well as any other on the internet) to find functions that can be used to manipulate 
dictionaries.
`https://docs.python.org/3/library/stdtypes.html#typesmapping`

## Running the Applications (on command line)
Open 2 terminals.  
In the first terminal run:  
`python3 server.py`    
Then, In the other terminal run:  
`python3 client.py`  

Two windows will open up, labelled client and server. The client window will have a `Register` button and a field to enter a username. If your code is written correctly, then pressing the button will send the username to the server, and the server wil respond with whether registration is successful or not. If successful, a login button will appear. If the login process is successful then finally a button to request the client registry will appear. Message transmision and reception will be printed on to the screens.

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of the client, sending messages to register, login and request the registry. This is done in the file `client_logic.py`.
2. Implement the server-side logic of responding to different requests of the client. This is done in the file `server_logic.py`.