# asyncio_coroutine.py
import asyncio


async def coroutine():
    print('now in coroutine')


event_loop = asyncio.get_event_loop()
print('start coroutine')
coro = coroutine()
print(coro)
print('enter event loop')
event_loop.run_until_complete(coro)
print('close event loop')
event_loop.close()
