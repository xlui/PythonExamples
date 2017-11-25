# asyncio_future_event_loop.py
import asyncio


def set_result(future, result):
    print('setting future result to {}'.format(result))
    future.set_result(result)


event_loop = asyncio.get_event_loop()
future = asyncio.Future()
print('scheduling set_result')
event_loop.call_soon(set_result, future, 'the result')
print('entering event loop')
ret = event_loop.run_until_complete(future)
print('returned result: {}'.format(ret))
event_loop.close()

print('future result: {}'.format(future.result()))
