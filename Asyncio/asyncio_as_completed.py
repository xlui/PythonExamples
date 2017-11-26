# asyncio_as_completed.py
import asyncio


async def phase(i):
    print('now in phase {}'.format(i))
    await asyncio.sleep(0.5 - (0.1 * i))
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)


async def main(phase_count):
    print('now in main')
    phases = [phase(i) for i in range(phase_count)]
    print('waiting for phases to complete')
    results = []
    for completed_task in asyncio.as_completed(phases):
        answer = await completed_task
        print('received answer {}'.format(answer))
        results.append(answer)
    print('results: {}'.format(results))
    return results


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(3))
event_loop.close()
