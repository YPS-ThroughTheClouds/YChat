# """
# Description:
# In this function, write the actions a server should perform when it receives a message to forward to another client.
# 
# To Do:
# You should complete the following steps:
# 1. Check if the sending client has already logged in
# 2. Check if the receiving client is logged in
# 3. If so, forward the message
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# receiver_username (String): the username of the receiving client
# msg (String): the message to be sent to the receiving client
#
# """
async def forward_message_to_client(server, receiver_username, msg):
    # Hint: `await server.forward_message(username, msg)`
    # can be used to forward a message to client `username`

    # Hint: server.logged_in() returns true if the sending client has already logged in
    # Hint: server.user_is_logged_in(username) returns true if a client with `username` is logged in

    # `*** start ***`  

    if server.logged_in() & server.user_is_logged_in(receiver_username):
        print("forwarding message to ", receiver_username, ", ", msg)
        await server.forward_message(receiver_username, msg)
    
    # `*** end ***`  
