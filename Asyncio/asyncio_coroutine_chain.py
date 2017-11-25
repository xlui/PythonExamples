# asyncio_coroutine_charin.py
import asyncio


async def call_first():
    print('now in first')
    return 'first'


async def call_second(arg):
    print('now in second')
    return 'second with arg: {}'.format(arg)


async def coroutine():
    print('now in coroutine')
    print('wait for function first')
    ret1 = await call_first()
    print('wait for function second')
    ret2 = await call_second(ret1)
    return ret1, ret2


event_loop = asyncio.get_event_loop()
ret = event_loop.run_until_complete(coroutine())
print('result value: {}'.format(ret))
event_loop.close()
