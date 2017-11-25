# asyncio_future_callback.py
import asyncio
from asyncio import Future
import functools


def callback(_future, n):
    print('{}: future done: {}'.format(n, _future.result()))


async def register_callbacks(_future):
    """:type _future: Future"""
    print('registering callbacks on future')
    _future.add_done_callback(functools.partial(callback, n=1))
    _future.add_done_callback(functools.partial(callback, n=2))


async def main(_future):
    """:type _future: Future"""
    await register_callbacks(_future)
    print('setting result of future')
    _future.set_result('the result')


event_loop = asyncio.get_event_loop()
future = asyncio.Future()
event_loop.run_until_complete(main(future))
event_loop.close()
