# echo_server.py

import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 10000)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger('main')
event_loop = asyncio.get_event_loop()


class EchoServer(asyncio.Protocol):
    def __init__(self) -> None:
        super().__init__()

    def connection_made(self, transport):
        """:type transport asyncio.Transport"""
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        fmt = 'EchoServer_{}_{}'.format(*self.address)
        self.log = logging.getLogger(fmt)
        self.log.debug('connection accepted')

    def data_received(self, data):
        self.log.debug('received {}'.format(data))
        self.transport.write(data)
        self.log.debug('sent {}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, exc):
        if exc:
            self.log.error('Error: {}'.format(exc))
        else:
            self.log.debug('closing')
        super().connection_lost(exc)


if __name__ == '__main__':
    factory = event_loop.create_server(EchoServer, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(factory) # type: asyncio.AbstractServer
    logger.debug('start up on {} port {}'.format(*SERVER_ADDRESS))
    try:
        event_loop.run_forever()
    finally:
        logger.debug('closing server')
        server.close()
        print(type(server))
        event_loop.run_until_complete(server.wait_closed())
        logger.debug('closing event loop')
        event_loop.close()
