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
`send_message(self, message)`  
`receive_message(self)`  

So, for example, to send a message from the server, you would write:  
`await server.send_message("Ping")`  
To receive a message, you would write:  
`msg = await server.receive_message()` 

Whenever you use the send or receive messages, you must write `await` before, as it indicates that messages can be sent or received asynchronously.

## Running the Applications (on command line)
Open 2 terminals.  
In the first terminal run:  
`python3 server.py`    
Then, In the other terminal run:  
`python3 client.py`  

Two windows will open up, labelled client and server. The client window will have a `Ping` button. If your code is written correctly, then pressing the button will send a `Ping` message to the server, and the server wil respond with a `Pong` message. Message transmision and reception will be printed on to the screens.

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of sending a **Ping** message to the server. This is done in the file `client_logic.py`. Run your client application against the server file we've provided to check your client is working correctly.
2. Implement the server-side logic of sending a **Pong** message whenever a **Ping** is received. This is done in the file `server_logic.py`. To test, run your own client implementation against your server implementation.