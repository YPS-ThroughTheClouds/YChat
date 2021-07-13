# """
# Description:
# In this function, write the actions a server should perform when it receives a message. 
#
# To Do:
# You should complete the following steps:
# 1. Check if the received message is a "Ping" or a "Pong"
# 2. If so, forward the message to the other client
#
# Parameters:
# server (Server): A handle to a server object that provides functions to send and receive messages.
# msg (string): the message the server has just received from a client
# 
# """
async def server_logic(server, msg):
    # `*** start ***`  

    if (msg == "Ping") | (msg == "Pong"):
        await server.forward_message(msg)

    # `*** end ***`
