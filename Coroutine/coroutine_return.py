# coroutine_return.py
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


if __name__ == '__main__':
    coro = averager()
    next(coro)              # 预激协程
    coro.send(10)
    coro.send(30)
    coro.send(5)
    coro.send(None)
