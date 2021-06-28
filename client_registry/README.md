# Multi-client PingPong Application

## Objective
In this application, we run two client programs and one server program in which the following steps should occur:
1. Client1 sends a **Ping** message to the server.
2. The server receives the message and forwards it to client2.
4. Client2 receives the message and sends a **Pong** message in response to the server.
2. The server receives the message and forwards it to client1.

## Tasks
You can complete this assignment in two steps:
1. Implement the client-side logic of client2, sending a **Pong** message to the server in response to a **Ping**. This is done in the file `client2_student.py`.
2. Implement the server-side logic of forwarding the messages between the two clients. This is done in the file `server_student.py`.

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

For the server we also provide another function:  
`forward_message(self, Message)`  
which takes a message and sends it to the other client.

## Running the Applications (on command line)
Open 3 terminals and run the programs in the following order.  
In the first terminal run:  
`python server_student.py` or `python server.py`    
In the second terminal run:  
`python client2_student.py` or `python client2.py`  
In the third terminal run:  
`python client1.py`
You should see the **Ping** and **Pong** messages printed in the terminals. 

## Notes for Anurag
`server_student.py` and `client2_student.py` are the files you have to fill out yourself. You can run them against `server.py` and `client2.py`. They all use loopback, and the port number is defined at the top of `utils2.py`.  

