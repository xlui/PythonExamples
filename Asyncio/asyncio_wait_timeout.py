# asyncio_wait_timeout.py
import asyncio


async def phase(i):
    print('now in phase {}'.format(i))
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print('phase {} canceled'.format(i))
        raise
    else:
        print('done with phase {}'.format(i))
        return 'phase {} result'.format(i)


async def main(phase_count):
    print('now in main')
    phases = [phase(i) for i in range(phase_count)]
    print('wait 0.1s for phases to complete')
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print('{} completed and {} pending'.format(len(completed), len(pending)))
    if pending:
        print('canceling tasks')
        for _p in pending:
            _p.cancel()
    print('exiting main')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(3))
event_loop.close()
