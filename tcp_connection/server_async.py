import asyncore
import socket

class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('',port))
        self.listen(5)
    def handle_accept(self):
        newSocket, address = self.accept(  )
        print "Connected from", address
        SecondaryServerSocket(newSocket)

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def handle_read(self):
        receivedData = self.recv(8192)
        print receivedData
        # if receivedData: self.send(receivedData)
        # else: self.close(  )
    def handle_close(self):
        print "Disconnected from", self.getpeername(  )
        self.close()

MainServerSocket(8881)
asyncore.loop()