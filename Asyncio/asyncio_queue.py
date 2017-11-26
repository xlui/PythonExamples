# asyncio_queue.py

import asyncio


async def consumer(n, _queue):
    """:type _queue asyncio.Queue"""
    # print('consumer {}: waiting for item'.format(n))
    while True:
        print('consumer {}: waiting for item'.format(n))
        item = await _queue.get()
        print('consumer {}: has item {}'.format(n, item))
        if item is None:
            _queue.task_done()
            break
        else:
            await asyncio.sleep(.01 * item)
            _queue.task_done()
    print('consumer {}: ending'.format(n))


async def producer(_queue, workers):
    """:type _queue asyncio.Queue"""
    print('producer: starting')

    for i in range(workers * 3):
        await _queue.put(i)
        print('producer: add task {} to queue'.format(i))

    print('producer: adding stop signals to the queue')
    for i in range(workers):
        await _queue.put(None)
    print('producer: waiting for queue to empty')
    await _queue.join()
    print('producer: ending')


async def main(loop, _consumers):
    queue = asyncio.Queue(maxsize=_consumers)
    consumers = [loop.create_task(consumer(i, queue)) for i in range(_consumers)]
    prod = loop.create_task(producer(queue, _consumers))
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop, 2))
event_loop.close()
