# coroutine_average.py
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
    next(coro)                  # 预激协程
    print(coro.send(10))
    print(coro.send(20))
    print(coro.send(5))
    coro.close()
