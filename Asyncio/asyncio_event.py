# asyncio_event.py
import asyncio
import functools


def set_event(event):
    """:type event asyncio.Event"""
    print('setting event in callback')
    event.set()


async def coroutine1(event):
    """:type event asyncio.Event"""
    print('coroutine 1 waiting for event')
    await event.wait()
    print('coroutine 1 triggered')


async def coroutine2(event):
    """:type event asyncio.Event"""
    await event.wait()
    print('coroutine 2 triggered')


async def main(loop):
    event = asyncio.Event()
    print('event start state: {}'.format(event.is_set()))
    loop.call_later(0.1, functools.partial(set_event, event))
    await asyncio.wait([
        coroutine1(event),
        coroutine2(event),
    ])
    print('event end state: {}'.format(event.is_set()))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
