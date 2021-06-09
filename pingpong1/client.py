from pingpong1.utils import MessageType, Client

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
client = Client.init()

# Send a packet over the TCP connection
client.send_message(MessageType.Ping)

# Receive a packet over the TCP connection
msg = client.recv_message()

# should process received message and check its a Pong


