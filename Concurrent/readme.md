# cocurrent.futures 模块

`future` 是 `concurrent.futures` 模块和 `asyncio` 包的重要组件。从 Python3.4 起，标准库中有两个名为 `Future` 的类：`concurrent.futures.Future` 和 `asyncio.Future`。这两个类的作用相同：两个 `Future` 类的实例都表示可能已经完成或者尚未完成的延迟计算。

`future` 封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或抛出异常）后可以获得结果（或异常）。

通常情况下，我们不应该自己创建 `future`，只能由并发框架（`concurrent.futures` 或 `asyncio`）实例化。原因很简单：`future` 表示终将发生的事情，而确定某件事会发生的唯一方式是执行时间已经排定。因此，只有排定把某件事交给 `concurrent.future.Executor` 子类处理时，才会创建 `concurrent.futures.Future` 实例。例如，`Executor.submit()` 方法的参数是一个可调用对象，调用这个方法后会为传入的可调用对象排期，并返回一个 `future`。

两种 `future` 都有 `.done()` 方法，这个方法不会阻塞，返回值是布尔值，指明 `future` 链接的可调用对象是否已经执行。

都有 `.add_done_callback()` 方法，这个方法只有一个参数，类型是可调用对象，`future` 运行结束后会调用指定的可调用对象。

此外，还有 `.result()` 方法。在 `future` 运行结束后调用的话，这个方法在两个 `Future` 类中的作用相同：返回可调用对象的结果，或者重新抛出执行可调用对象时抛出的异常。如果 `Future` 没有运行结束，`.result()` 方法在两个 `Future` 类中的行为差别很大。对于 `concurrent.futures.Future` 实例来说，调用 `f.result()` 方法会阻塞调用方所在的线程，直到有结果可以返回。此时，`result` 方法可以接收可选的 `timeout` 参数，如果在指定的时间内 `future` 没有运行完毕，会抛出 `TimeoutError` 异常。而 `asyncio.Future.result()` 方法不支持设定超时时间，在那个库中获取结果最好使用 `yield from` 结构。

## 使用 concurrent.futures 模块启动线程

```python
from concurrent import futures
with futures.ThreadPoolExecutor(3) as executor:
    res = executor.map(func, *args)
```

## 手动处理结果

```python
from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []
    for cc in sorted(cc_list):
        future = executor.submit(func, cc)
        to_do.append(future)
        msg = 'Scheduled for {}: {}'
        print(msg.format(cc, future))

    results = []
    for future in futures.as_completed(to_do):
        res = future.result()
        msg = '{} result: {!r}'
        print(msg.format(future, res))
        results.append(res)
```

首先调用 `Executor.submit()` 为每一个 `download_one` 函数排序。然后循环从 `futures.as_completed(to_do_futures)` 中获取执行完毕的 `future`。最后调用 `future.result()` 获取 `download_one` 函数执行的结果。

## 重要！！！

**标准库中所有执行阻塞型 I/O 操作的函数，在等待操作系统返回结果时都会释放 GIL**  
**标准库中所有执行阻塞型 I/O 操作的函数，在等待操作系统返回结果时都会释放 GIL**  
**标准库中所有执行阻塞型 I/O 操作的函数，在等待操作系统返回结果时都会释放 GIL**  

这说明，尽管有 GIL，Python 线程还是可以在 I/O 密集型应用中发挥作用。

我认为这一点是协程与异步编程的基础。

## 使用 concurrent.futures 模块启动进程

只需要将上面代码中：

```
with futures.ThreadPoolExecutor(workers) as executor
``` 

换为：

```
with futures.ProcessPoolExecutor() as executor
```

对于简单的用途来说，这两个实现 `Executor` 接口的类唯一值得注意的区别是，`ThreadPoolExecutor.__init__` 方法需要 `max_worker` 参数，指定线程池中线程的数量。在 `ProcessPoolExecutor` 类中，那个参数是可选的，而且大多数情况下不使用 —— 默认值是 `os.cpu_count()` 函数返回的 CPU 数量。

## 实验 Executor.map 方法

若想并发运行多个可调用对象，最简单的方式是使用 `Executor.map` 方法。下面的实例演示了 `Executor.map` 方法的某些运行细节。

```python
from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5))
    display('results: ', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
```

`Executor.map` 函数易于使用，不过有个特性能有用，也可能没用，具体情况取决于需求：这个函数返回结果的顺序与调用开始的顺序一致。如果第一个调用生成结果用时 10 秒，而其他调用只用 1 秒，代码会阻塞 10 秒，获取 `map` 方法返回的生成器产出的第一个结果。在此之后，获取后续结果不会阻塞，因为后续的调用已经结束。如果必须等到获取所有结果后再处理，这种行为没问题；不过，通常更可取的方式是，不管提交的顺序，只要有结果就获取。为此，要把 `Executor.submit` 方法和 `futures.as_completed` 函数结合起来使用，就像上面**手动处理结果**中的程序一样。
