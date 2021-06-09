from pingpong1.utils import MessageType, Server

# Set up the TCP connection
# currently loopback, but we can make this more generic to take any server IP address
server = Server.init()
# Receive a packet over the TCP connection
msg = server.recv_message()
# Should check that received message is ping, then send a pong
server.send_message(MessageType.Pong)




