# asyncio_coroutine_return.py
import asyncio


async def coroutine():
    print('now in coroutine')
    return 'result'


event_loop = asyncio.get_event_loop()
ret = event_loop.run_until_complete(coroutine())
print('coroutine returned: {}'.format(ret))
event_loop.close()
