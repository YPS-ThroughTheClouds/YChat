from pingpong2.utils import MessageType, init_server, server_recv_message, server_forward_message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
init_server()

while 1:
    # Receive a packet over the TCP connection from a client
    sender, receiver, msg = server_recv_message()

    # check to see if we have a TCP connection with the receiver

    # Forward message to intended recipient
    server_forward_message(sender, receiver, MessageType.Pong)





