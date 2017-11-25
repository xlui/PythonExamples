# 协程

> 如果 Python 书籍有一定的指导作用，那么（协程就是）文档最匮乏、最鲜为人知的 Python 特性，因此表面上看是最无用的特性。

字典为动词 “to yield” 给出了两个释义：产出和让步。对于 Python 生成器中的 `yield` 来说，这两个含义都成立。 `yield item` 这行代码会产出一个值，提供给 `next(...)` 的调用方；此外，还会做出让步，让 `next(...)` 调用方继续工作，直到需要使用另一个值时再调用 `next()`。调用方会从生成器中拉取值。

从句法上看，协程和生成器类似，都是定义体中包含 `yield` 关键字的**函数**。可是，在协程中，**yield 通常出现在表达式的右边**（例如：`data = yield`)，可以产出值，也可以不产出--如果 `yield` 关键字后面没有表达式，那么生成器产出 `None`。协程可能从调用方接收数据，不过调用方把数据提供给协程使用的是 `.send(data)` 方法，而不是 `next(...)` 函数。通常，调用方会把值推送给协程。

`yield` 关键字甚至可以不接受或者传出数据。不管数据怎么流动，`yield` 都是一种流程控制工具，使用它可以实现协作式多任务：协程可以把控制器让步给中心调度程序，从而激活其他的协程。

## 一个简单的协程

```python
# coroutine
def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)


my_coro = simple_coroutine()
print(my_coro)              # 与创建生成器的方式一样，调用协程函数得到生成器对象
next(my_coro)               # 预激协程
my_coro.send(47)            # 向协程发送数据，协程中 x 接收到通过 send 函数发送的数据。
# 最后控制权流动到协程定义体的末尾，导致生成器像往常一样抛出 StopIteration 异常
```

输出：

```
<generator object simple_coroutine at 0x0000017DB0FE11A8>
-> coroutine started
-> coroutine received: 47
Traceback (most recent call last):
  ...
StopIteration
```

协程可以身处四个状态之一。当前状态可以使用 `inspect.getgeneratorstate(...)` 函数确定，该函数会返回下述字符串中的一个：

状态|说明
:---:|:---:
GEN_CREATED|等待开始执行
GEN_RUNNING|解释器正在执行
GEN_SUSPENDED|在 yield 表达式处暂停
GEN_CLOSED|执行结束

因为 `send` 方法的参数会成为暂停的 `yield` 表达式的值，所以，仅当协程处于暂停状态时才能调用 `send` 方法。所以，在开始发送数据前，需要预激协程（一般使用 `send(None)` 或者 `next(my_coro)`），让协程从 `'GEN_CREATED'` 状态转到 `'GEN_SUSPENDED'`。

## 示例：使用协程计算移动平均值

```python
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
```

输出结果：

```
10.0
15.0
11.666666666666666
```

`averager()` 函数中的无限循环表明，只要调用方不断把值发给这个协程，他就会一直接收值，然后生成结果。

仅当调用方在协程上调用 `.close()` 方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止。

## 通过装饰器预激协程

```python
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
```

输出结果：

```
do primer
GEN_SUSPENDED
10.0
15.0
11.666666666666666
```

使用 `yield from` 句法调用协程时，会自动预激，因此与示例中的 `@coroutine` 等装饰器不兼容。Python 标准库里的 `@asyncio.coroutine` 装饰器不会预激协程，因此它创建的协程能兼容 `yield from` 句法。

## 终止协程和异常处理

```python
>>> from Coroutine.coroutine_pre-activation import averager
>>> coro = averager()
do primer
>>> coro.send(40)
40.0
>>> coro.send(59)
49.5
>>> coro.send('spam')
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for +=: 'float' and 'str'
>>> coro.send(12)
Traceback (most recent call last):
  ...
StopIteration
```

当发送的值不是数字时协程内出现异常，协程会停止，并且异常冒泡到调用方。如果试图重新激活协程，会抛出 StopIteration 异常。

可以在协程中 `yield` 语句周围加上 `try/except` 块来捕获可能出现的异常，或者给异常附加信息，然后向上冒泡，或者在出现不可预料的异常时直接停止程序：

```py
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
```

不论何时，只要出现了未处理的异常，协程的状态都会变成 `'GEN_CLOSED'`，所以不能再重新激活协程。

## 让协程返回值

```python
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
```

运行结果：

```
Traceback (most recent call last):
  ...
StopIteration: Result(count=3, average=15.0)
```

通过判断变量 `term` 是否为 `None` 来决定是否终止协程，终止协程时返回一个 Result 类对象，附加在 StopIteration 异常的信息中。

## 使用 yield from

`yield from` 是一种全新的语言结构。它的作用比 `yield` 多很多，以至于人们认为继续使用它会引起误解。于是在 Python3.5 中，一向以十分保守态度对待关键字的 Guido 也同意了引入关键字 `async` 和 `await`。

关于 `async` 和 `await` 的讨论放到之后的 `asyncio` 中，在 Python3.6 中依旧可以使用 `yield from` 句法。

`yield from` 的一个作用就是简化 `for` 循环中的 `yield` 表达式：

```py
>>> def gen():
...     for c in 'AB':
...         yield c
...     for i in range(1, 3):
...         yield i
>>> list(gen())
['A', 'B', 1, 2]
```

可以改写为：

```py
>>> def gen():
...     yield from 'AB'    
...     yield from range(1, 3)
>>> list(gen())
['A', 'B', 1, 2]
```

可以看到 `yield from` 自动迭代了 `iterable` 对象，并且像 `for` 循环一样内部解决了 协程/生成器 运行结束时产生的 `StopIteration` 异常。

`yield from x` 对 x 对象所做的第一件事是：调用 `iter(x)`，从中获取迭代器。因此，x 可以是任何可迭代对象（iterable）。

但是，如果 `yield from` 的功能仅仅是替代产出值的嵌套 `for` 循环，这个结构可能不会被添加到 Python 中。

`yield from` 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。有了这个结构，协程就可以通过以前不可能的方式委托职责。

为了方便说明，PEP 380 使用了一些专门的术语（请务必理解或者熟悉，后文这三个术语会大量出现）。

**委派生成器**  
&nbsp;&nbsp;&nbsp;&nbsp;包含 `yield from <iterable>` 表达式的生成器函数  
**子生成器**  
&nbsp;&nbsp;&nbsp;&nbsp;从 `yield from` 表达式中 `<iterable>` 部分获取的生成器。  
**调用方**  
&nbsp;&nbsp;&nbsp;&nbsp;调用委派生成器的客户端代码。  

通俗的理解就是，调用方调用委派生成器，委派生成器中有 `yield from <iterable>` 代码，其中 `<iterable>` 部分代码是可以获取的子生成器。通过委派生成器中的 `yield from`，调用方和子生成器建立了联系，可以直接进行数据/异常传递。其中委派生成器 `yield from` 语句的值就是子生成器的返回值。

下面这个示例是从字典中读取男女生体重和身高，然后将数据发送给 `averager()` 协程，最后生成一个报告。

```py
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
```

输出：

```
 9 boys  averaging 40.42kg
 9 boys  averaging 1.39m
10 girls averaging 42.04kg
10 girls averaging 1.43m
```

下面对上面的程序进行解析，来对 `yield from` 句法的用途有一个直观地认识。

还记得前面说过的调用方、委派生成器和子生成器吗？在这个程序里面，`main()` 函数是调用方，`grouper()` 函数是委派生成器，`averager()` 函数是子生成器。

`main()` 函数从 `data` 字典中读取数据，然后将数值部分交给委派生成器 `grouper()` 处理，通过 `next()` 函数预激委派生成器，委派生成器在 `yielf from` 处暂停，等待子生成器返回数据。此时，委派生成器变成了 `main()` 函数和 `averager()` 函数的通道，两者可以不经过委派生成器直接互传数据。可以看到的是，在 `main()` 函数中，直接通过 `.send()` 向 `averager()` 发送数据而没有通过委派生成器 `grouper()`。

委派生成器 `grouper()` 的 `yield from` 语句会接收子生成器 `averager()` 返回的值，存入 `results` 字典中的 `key` 变量所指的键中，然后委派生成器中的循环进入下一步，并在 `yielf from` 处再次暂停，等待子生成器返回的值。所以，如果在 `main()` 函数中没有最后发送 `None` 的话（`group.send(None)`），子生成器 `averager()` 就不会停止并返回值，`yield from` 最终得到的结果会是空的。

当一个协程丢失引用时，会被垃圾回收程序回收（在本例中是 main 函数的 `for` 循环的一次循环执行完毕，前一个 grouper 实例以及它创建的尚未终止的 averager 子生成器实例被垃圾回收程序回收）。

## yield from 的实现细节

通过读代码来理解 `yield from` 的实现应该是最快的。

下面列出的代码是**委派生成器中**下面一行代码的简单扩充（伪代码）：

```
RESULT = yielf from EXPR
```

```
_i = iter(EXPR)
try:
    _y = next(_i)
except StopIteration as _e:
    _r = _e.value
else:
    while 1:
        _s = yield _y
        try:
            _y = _i.send(_s)
        except StopIteration as _e:
            _r = _e.value
            break

RESULT = _r
```

其中：  
_i 是迭代器，即子生成器  
_y 是子生成器产出的值  
_r 是最终的结果，即 `yield from` 表达式的值  
_s 是调用方发送给子生成器的值，会转发给子生成器  
_e 是异常对象，伪代码中始终是 StopIteration 实例  

伪代码首先对子生成器进行了预激，并将结果保存在 `_y` 中，作为产出的第一个值。

然后是一个无限循环，首先通过 `_s = yield _y` 将 `_y` 产出给调用方。

然后接收调用方发送的值 `_s`。

然后通过 `_i.send(_s)` 将 `_s` 发送给子生成器。

这就是调用方和子生成器直接进行通信的关键，调用方发送（通过 `.send()` 函数）给委托生成器的数据（`_s`) 被直接转发给了子生成器。

伪代码中还处理了 `StopIteration` 异常，子生成器返回的值就被包装在 `StopIteration` 异常中，通过将他解包装并赋给 `Result`，这样我们在使用的时候就不需要关心 `StopIteration` 异常了。

至于完整版的伪代码这里就不分析了，完整版的多了几个异常处理，并且区分了 `_s` 是否为 None 的情况。

正如伪代码中所述，`yield from` 会自动预激子生成器，所以才会在前面说用于自动预激的装饰器与 `yield from` 结构不兼容。

通过使用 `yield from` 可以有效避免类似 js 中回调地狱的情况，因为我们所有的异步调用都在同一个函数中，并且异常处理也变得十分简便。

`yield from` 的大量使用都是基于 `asyncio` 模块的异步编程，因此要有有效的事件循环才能运行。
