# coroutine_pre-activation.py
from functools import wraps


def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        print('do primer')
        next(gen)
        return gen
    return primer


@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


if __name__ == '__main__':
    coro = averager()
    from inspect import getgeneratorstate
    print(getgeneratorstate(coro))
    print(coro.send(10))
    print(coro.send(20))
    print(coro.send(5))
