# asyncio_lock.py
import asyncio
import functools


def unlock(lock):
    """:type lock asyncio.Lock"""
    print('callback releasing lock')
    lock.release()


async def coroutine1(lock):
    """:type lock asyncio.Lock"""
    print('coroutine 1 waiting for the lock')
    with await lock:
        print('coroutine 1 acquired lock')
    print('coroutine 1 released lock')


async def coroutine2(lock):
    """:type lock asyncio.Lock"""
    print('coroutine 2 waiting for the lock')
    await lock
    print('coroutine 2 acquired lock')
    print('coroutine 2 released lock')
    lock.release()


async def main(loop):
    lock = asyncio.Lock()
    print('acquiring the lock before starting coroutines')
    await lock.acquire()
    print('lock acquired: {}'.format(lock.locked()))

    loop.call_later(0.1, functools.partial(unlock, lock))

    print('waiting for coroutines')
    await asyncio.wait([
        coroutine1(lock),
        coroutine2(lock),
    ])


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
