# asyncio_gather.py
import asyncio


async def phase1():
    print('now in phase 1')
    await asyncio.sleep(2)
    print('done with phase 1')
    return 'phase 1 result'


async def phase2():
    print('now in phase 2')
    await asyncio.sleep(1)
    print('done with phase 2')
    return 'phase 2 result'


async def main():
    print('now in main')
    print('waiting for phases to complete')
    results = await asyncio.gather(
        phase1(),
        phase2(),
    )
    print('results: {}'.format(results))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.close()
