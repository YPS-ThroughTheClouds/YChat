# """
# Description:
# In this function, write the steps client 2 should take when it receives a message from the server.
#
# To Do:
# You should complete the following steps:
# 1. Check if the received message is a "Ping"
# 2. If so, send a "Pong" message to the server
#
# Parameters:
# client (Client): A handle to a client object that provides functions to send and receive messages.
# msg (string): the message the client has just received from the server
#  
# """
async def client_sends_a_pong(client, msg):
    # `*** start ***`  

    # Hint: You can send a message using the `await client.send_message(msg)` function.
    if msg == "Ping":
        await client.send_message("Pong")

    # `*** end ***`
