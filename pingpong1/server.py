from pingpong1.utils import MessageType, init_server, recv_message, send_message

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
init_server()
# Receive a packet over the TCP connection
msg = recv_message()
# Should check that received message is ping, then send a pong
send_message(MessageType.Pong)




