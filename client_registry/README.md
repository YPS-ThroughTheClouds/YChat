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
In addition to send and receive functions, we also provide functions that complete different server tasks such as adding clients to a registry and logging them in.  
`server.registered()` returns true if the client has already been registered  
`server.username_exists(username)` returns true if the given username is taken  
`server.register_user(username)` can be used to register a client  
`server.registered()` returns true if the client has already been registered  
`server.username_matches_record(username)` returns true if the given username matches the registered one  
`server.log_in_client(username)` can be used to log in a client  
`server.logged_in()` returns true if the client has already logged in  


## Running the Applications (on command line)
Open 2 terminals.  
In the first terminal run:  
`python3 server.py`    
Then, In the other terminal run:  
`python3 client.py`  

Two windows will open up, labelled client and server. The client window will have a `Register` button and a field to enter a username. If your code is written correctly, then pressing the button will send the username to the server, and the server wil respond with whether registration is successful or not. If successful, a login button will appear. If the login process is successful then finally a button to request the client registry will appear. Message transmision and reception will be printed on to the screens.

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of the client, sending messages to register, login and request the registry. This is done in the file `client_student.py`.
2. Implement the server-side logic of responding to different requests of the client. This is done in the file `server_student.py`.