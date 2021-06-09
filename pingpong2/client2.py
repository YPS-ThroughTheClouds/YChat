from pingpong2.utils import MessageType, init_client2, client_recv_message, client_send_message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client2 = init_client2()

# Receive a packet over the TCP connection
msg, client1 = client_recv_message()

# should process received message and check its a Ping

# Send a packet over the TCP connection to be sent to client 2
client_send_message(client2, client1, MessageType.Pong)

