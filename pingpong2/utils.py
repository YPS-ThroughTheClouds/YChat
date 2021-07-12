localhost = '127.0.0.1'
remotehost = "128.96.32.1"  # TO DO: Change this!!
host = localhost
port = 8888
sockets = []


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
        print("sending ", data)
        self.writer.write(data.encode())
        await self.writer.drain()

    async def forward_message(self, msg):
        index = get_other_client(self.writer.get_extra_info('peername'))
        if len(index) != 0:
            print("sending to ", sockets[index[0]].writer.get_extra_info('peername'))
            await sockets[index[0]].send_message(msg)


def get_other_client(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x != y.writer.get_extra_info('peername')]
    indexes = get_indexes(peername, sockets)
    return indexes


def remove_from_socket_list(peername):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y.writer.get_extra_info('peername')]
    del sockets[get_indexes(peername, sockets)[0]]
