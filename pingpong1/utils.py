
localhost = '127.0.0.1'
port = 8888


class Client:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def receive_message(self):
        data = await self.reader.read(100)
        message = data.decode()
        addr = self.writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
        if (message == "Ping") | (message == "Pong"):
            return message
        else:
            return "Uknown message"

    async def send_message(self, data):
        self.writer.write(data.encode())
        await self.writer.drain()



class Server:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def receive_message(self):
        data = await self.reader.read(100)
        message = data.decode()
        addr = self.writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
        if (message == "Ping") | (message == "Pong"):
            return message
        else:
            return "Uknown message"

    async def send_message(self, data):
        self.writer.write(data.encode())
        await self.writer.drain()
