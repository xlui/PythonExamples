# asyncio_task.py
import asyncio


async def func_task():
    print('now in function task')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(func_task())
    print('waiting for {!r}'.format(task))
    ret = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(ret))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
