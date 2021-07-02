# """
# Description:
# In this function, write the steps a client should take to send a message to the server.
#
# To Do:
# You should complete the following steps:
# 1. Send a "Ping" message
#
# Parameters:
# client (Client): A handle to a client object that provides functions to send and receive messages.
# 
# """
async def client_sends_a_ping(client):
    # `*** start ***`  
    
    # Hint: You can send a message using the client.send_message(msg) function.
    await client.send_message("Ping")
    
    # `*** end ***`  


