from pingpong2.utils import MessageType, init_client1, client_recv_message, client_send_message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client1 = init_client1()
client2 = "random_ip"

# Send a packet over the TCP connection to be sent to client 2
# maybe client should be a class, then we don't have to specify senders address?
client_send_message(client1, client2, MessageType.Ping)

# Receive a packet over the TCP connection
msg, sender = client_recv_message()

# should process received message and check its a Pong


