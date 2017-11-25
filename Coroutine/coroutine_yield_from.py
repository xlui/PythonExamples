# coroutine_yield_from
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    """计算平均值的协程
    只有调用方调用 `.send(None)` 或者 `.close()` 方法时才会停止 while 循环并返回结果
    :return: Result 类对象，属性 count 是数量，属性 average 是平均值
    """
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


def grouper(results, key):
    """委派生成器，作为调用方与子生成器联系的纽带。

    :param results: 结果字典
    :param key: 键
    :return: None
    """
    while True:
        results[key] = yield from averager()


def main(data):
    """ 调用方，调用委派生成器，委派生成器通过 `yield from` 打开调用方与子生成器的链接
    这时，调用方可以通过 `.send()` 方法直接向子生成器发送数据

    :param data: 原始数据
    :return:  None
    """
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)
