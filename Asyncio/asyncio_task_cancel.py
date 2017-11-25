# asyncio_task_cancel.py
import asyncio


async def func_task():
    print('now in function task')
    return 'task result'


async def main(loop):
    print('creating task')
    task = loop.create_task(func_task())

    print('canceling task')
    task.cancel()

    print('canceled task {!r}'.format(task))

    try:
        await task
    except asyncio.CancelledError:
        print('caught error from canceled task')
    else:
        print('task result: {!r}'.format(task.result()))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
