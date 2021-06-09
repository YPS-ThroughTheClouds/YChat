from pingpong1.utils import MessageType, init_client, recv_message, send_message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
init_client()
# Send a packet over the TCP connection
send_message(MessageType.Ping)
# Receive a packet over the TCP connection
msg = recv_message()
# should process received message and check its a Pong


