# """
# Description:
# In this function, write the steps client 1 should take when it wants to send a "Ping" message to the server
#
# To Do:
# You should complete the following steps:
# 1. Send a "Ping" message to the server
#
# Parameters:
# client (Client): A handle to a client object that provides functions to send and receive messages.
#  
# """
async def client1_logic(client):
    # `*** start ***`  

    # Hint: You can send a message using the `await client.send_message(msg)` function.
    await client.send_message("Ping")


# `*** end ***`


# """
# Description:
# In this function, write the steps client 2 should take when it wants to send a "Pong" message to the server
#
# To Do:
# You should complete the following steps:
# 1. Send a "Pong" message to the server
#
# Parameters:
# client (Client): A handle to a client object that provides functions to send and receive messages.
#  
# """
async def client2_logic(client):
    # `*** start ***`  

    await client.send_message("Pong")

    # `*** end ***`
