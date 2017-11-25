# asyncio_future_await.py
import asyncio


def set_result(_future, _result):
    print('setting future result to {}'.format(_result))
    _future.set_result(_result)


async def main(loop):
    future = asyncio.Future()
    print('scheduling set_result')
    loop.call_soon(set_result, future, 'the result')
    ret = await future
    print('returned result: {}'.format(ret))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()