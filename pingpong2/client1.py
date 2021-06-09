from pingpong2.utils import MessageType, Client

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client1 = Client.init()

# Send a packet over the TCP connection to be sent to client 2
client1.send_message(MessageType.Ping)

# Receive a packet over the TCP connection
msg = client1.recv_message()

# should process received message and check its a Pong


