# Multi-client PingPong Application

## Objective
In this application, we run two client programs and one server program in which the following steps should occur:
1. Client1 sends a **Ping** message to the server.
2. The server receives the message and forwards it to client2.
4. Client2 receives the message and sends a **Pong** message in response to the server.
2. The server receives the message and forwards it to client1.

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

For the server we also provide another function:  
`await forward_message(self, Message)`  
which takes a message and sends it to the other client.

Whenever you use the send or receive messages, you must write `await` before, as it indicates that messages can be sent or received asynchronously.

## Running the Applications (on command line)
Open 3 terminals and run the programs in the following order.  
In the first terminal run:  
`python3 server.py`    
In the second terminal run:  
`python3 client2.py`  
In the third terminal run:  
`python3 client1.py`

Three windows will open up labelled server, client 1 and client 2. The client 1 window will have a `Ping` button. If your code is written correctly, then pressing the button will send a `Ping` message to the server, and the server wil forward it to client 2. Client 2 should send a `Pong` message in reponse, which the server will forward to client 1. Message transmision and reception will be printed on to the screens.

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of client2, sending a **Pong** message to the server in response to a **Ping**. This is done in the file `client2_student.py`.
2. Implement the server-side logic of forwarding the messages between the two clients. This is done in the file `server_student.py`.
