# Instant Messaging Application

## Objective

In this application, we run multiple client programs and one server program in which the following steps should occur:
1. Each client registers a username with the server.
2. Each client logs in to the server.
3. Each client requests the client registry from the server
4. Each client can then choose a recipient from the client registry and send them a message

The first three steps you have already completed in the previous assignment, so step 4 is the focus here.

## Software Interface

You are provided skeleton code, with portions you must fill in yourself. The portions you must fill are demarcated by 
these comments:  
`*** start ***`  
`*** end ***`  

For the Server, we provide the following function to forward messages between clients:  
`await server.forward_message(self, receiver_username, msg)`

In addition we provide the following functions:  
`server.logged_in()` returns true if the sending client has already logged in  
`server.user_is_logged_in(username)` returns true if a client with `username` is logged in  

## Running the Applications (on command line)

Open 2 terminals.  

In the first terminal run:  
`python3 server.py`    

Then, In the other terminal run:  
`python3 client.py`  

Two windows will open up, labelled client and server. The client window will have a `Register` button and a field to 
enter a username. If your code is written correctly, then pressing the button will send the username to the server, and 
the server wil respond with whether registration is successful or not. If successful, a login button will appear. If the 
login process is successful then finally a button to request the client registry will appear. Clicking on a client's 
name in the registry should open a chat box after which you can send and receive messages. Message transmision and 
reception will be printed on to the screens.

To test this application, you will have to open multiple terminals for clients.

## Tasks

This assignment has one step:
1. Implement the server-side logic of forwarding messages that clients want to send to each other. This is done in the 
   file `server_student.py`.