# echo_client.py

import asyncio
import functools
import logging
import sys

MESSAGES = [
    b'This is the message',
    b'It will be sent',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 10000)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger('main')
event_loop = asyncio.get_event_loop()


class EchoClient(asyncio.Protocol):
    def __init__(self, messages, future):
        """
        :type messages list
        :type future asyncio.Future
        """
        super(EchoClient, self).__init__()
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.future = future

    def connection_made(self, transport):
        """:type transport asyncio.Transport"""
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        fmt = 'connecting to {} port {}'.format(*self.address)
        self.log.debug(fmt)

        for msg in self.messages:
            transport.write(msg)
            self.log.debug('sending {}'.format(msg))

        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.debug('received {}'.format(data))

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('server closed connection')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)
        super().connection_lost(exc)


if __name__ == '__main__':
    _future = asyncio.Future()
    _factory = functools.partial(EchoClient, messages=MESSAGES, future=_future)
    _coroutine = event_loop.create_connection(_factory, *SERVER_ADDRESS)
    logger.debug('waiting for client to complete')
    try:
        event_loop.run_until_complete(_coroutine)
        event_loop.run_until_complete(_future)
    finally:
        logger.debug('closing event loop')
        event_loop.close()
