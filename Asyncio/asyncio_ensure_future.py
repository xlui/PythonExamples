# asyncio_ensure_future.py
import asyncio


async def wrapped():
    print('now in function wrapped')
    return 'result'


async def inner(task):
    print('now in function inner')
    print('inner: waiting for {!r}'.format(task))
    ret = await task
    print('inner: task return: {}'.format(ret))


async def outer():
    print('creating task')
    task = asyncio.ensure_future(wrapped())
    print('waiting for inner')
    await inner(task)
    print('inner returned')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(outer())
event_loop.close()
