# Simple Client-Server PingPong Application

## Objective
In this application, we run one client program and one server program in which the following steps should occur:
1. The client sends a **Ping** message to the server
2. The server receives the message, and checks that the message is a **Ping**
3. The server sends a **Pong** message to the client 

## Software Interface
You are provided skeleton code, with portions you must fill in yourself. The portions you must fill are demarcated by these comments:  
`*** start ***`  
`*** end ***`  

For the Server and Client, we provide the following two functions to send and receive messages:  
`send_message(self, Message)`  
`receive_message(self)`  

So, for example, to send a message from the server, you would write:  
`server.send_message(Message.Pong)`  
To receive a message, you would write:  
`msg = server.receive_message()` 

## Running the Applications (on command line)
Open 2 terminals.  
In the first terminal run:  
`python3 server.py`    
Then, In the other terminal run:  
`python3 client.py`  
You should see the **Ping** and **Pong** messages printed in the terminals. 

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of sending a **Ping** message to the server. This is done in the file `client_student.py`. Run your client application against the server file we've provided to check your client is working correctly.
2. Implement the server-side logic of sending a **Pong** message whenever a **Ping** is received. This is done in the file `server_student.py`. To test, run your own client implementation against your server implementation.