# asyncio_wait.py
import asyncio


async def phase(i):
    print('now in phase {}'.format(i))
    await asyncio.sleep(0.1 * i)
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)


async def main(phase_count):
    print('now in main')
    phases = [phase(i) for i in range(phase_count)]
    print('waiting for phases to complete')
    _futures, pending = await asyncio.wait(phases)
    results = [_future.result() for _future in _futures]
    print('results: {!r}'.format(results))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(3))
event_loop.close()
