# coroutine_exception_handling.py
class DemoException(Exception):
    """define a special exception for test"""


def demo_exception_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {}'.format(x))
        raise RuntimeError('This line should never run.')
