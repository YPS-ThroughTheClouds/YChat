from pingpong2.utils import MessageType, Server

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
server = Server.init()

while 1:
    # Receive a packet over the TCP connection from a client
    sender, msg = server.recv_message()

    # check to see the client that should receive the message
    # receiver = ...

    # Forward message to intended recipient
    server.forward_message(receiver, msg)





