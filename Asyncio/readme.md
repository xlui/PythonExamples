# asyncio

`asyncio` 包使用事件循环驱动的协程实现并发，这是 Python 中最大也是最具雄心壮志的库之一。

协程相对于线程和进程的优点是任务调度完全由用户自己把控，通过使用 `yield from foo`，将当前协程暂停，控制权移交给事件循环手中，再去驱动其他协程。当 `foo` 协程运行完毕后，将结果返回给暂停的协程，将其恢复。通过这种方式，避开了由操作系统调度可能出现的问题，同时也能高效利用 CPU。

## 启动一个 Coroutine

```py
# asyncio_coroutine.py
import asyncio


async def coroutine():
    print('now in coroutine')


event_loop = asyncio.get_event_loop()
print('start coroutine')
coro = coroutine()
print(coro)
print('enter event loop')
event_loop.run_until_complete(coro)
print('close event loop')
event_loop.close()
```

首先获取一个事件循环，然后用 `run_until_complete` 方法执行 `coroutine` 对象，当 coroutine 执行完并退出后，`run_until_complete` 也会随后退出。

```
start coroutine
<coroutine object coroutine at 0x00000247C5A47F68>
enter event loop
now in coroutine
close event loop
```

## 获取 Coroutine 的返回值

`run_until_complete` 会把 coroutine 的返回值当作自身的返回值返回给调用者：

```py
# asyncio_coroutine_return.py
import asyncio


async def coroutine():
    print('now in coroutine')
    return 'result'


event_loop = asyncio.get_event_loop()
ret = event_loop.run_until_complete(coroutine())
print('coroutine returned: {}'.format(ret))
event_loop.close()
```

执行结果：

```
now in coroutine
coroutine returned: result
```

## 链式调用 Coroutine

在一个 coroutine 函数中调用另一个 coroutine 函数，调用函数等待被调函数的返回结果：

```py
# asyncio_coroutine_charin.py
import asyncio


async def call_first():
    print('now in first')
    return 'first'


async def call_second(arg):
    print('now in second')
    return 'second with arg: {}'.format(arg)


async def coroutine():
    print('now in coroutine')
    print('wait for function first')
    ret1 = await call_first()
    print('wait for function second')
    ret2 = await call_second(ret1)
    return ret1, ret2


event_loop = asyncio.get_event_loop()
ret = event_loop.run_until_complete(coroutine())
print('result value: {}'.format(ret))
event_loop.close()
```

通过使用 await 等待 Coroutine 的返回结果。

```
now in coroutine
wait for function first
now in first
wait for function second
now in second
result value: ('first', 'second with arg: first')
```

## 使用生成器替代 Coroutine

`async` 和 `await` 是 Python3.5 引入的关键字，如果运行在 Python3.5 以下我们可以通过 `asyncio.coroutine` 装饰器和 `yield from` 来实现同样的功能：

```py
# asyncio_generator.py
import asyncio


@asyncio.coroutine
def call_first():
    print('now in first')
    return 'first'


@asyncio.coroutine
def call_second(arg):
    print('now in second')
    return 'second with arg: {}'.format(arg)


@asyncio.coroutine
def coroutine():
    print('now in coroutine')
    print('wait for function first')
    ret1 = yield from call_first()
    print('wait for function second')
    ret2 = yield from call_second(ret1)
    return ret1, ret2


event_loop = asyncio.get_event_loop()
ret = event_loop.run_until_complete(coroutine())
print('result value: {}'.format(ret))
event_loop.close()
```

执行结果：

```
now in coroutine
wait for function first
now in first
wait for function second
now in second
result value: ('first', 'second with arg: first')
```

# Task

Task 是跟事件循环交互的一种重要方式。Task 包装并追踪 Coroutine 的完成状态。Task 是 Future 的子类，因此其他 Coroutine 可以 `wait Task` 并在 Task 完成时获取 Task 的结果。

## 启动 Task

可以使用 `event_loop.create_task` 方法来创建一个 Task 实例：

```py
# asyncio_task.py
import asyncio


async def func_task():
    print('now in function task')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(func_task())
    print('waiting for {}'.format(task))
    ret = await task
    print('task completed {}'.format(task))
    print('return value: {}'.format(ret))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
```

可以看到 `await task` 得到的是 `func_task` 函数的返回值：

```
creating task
waiting for <Task pending coro=<func_task() running at ...>>
now in function task
task completed <Task finished coro=<func_task() done, defined at ...> result='the result'>
return value: the result
```

## 取消 Task

可以在 Task 完成之前取消 Task 的操作：

```py
# asyncio_task_cancel.py
import asyncio


async def func_task():
    print('now in function task')
    return 'task result'


async def main(loop):
    print('creating task')
    task = loop.create_task(func_task())

    print('canceling task')
    task.cancel()

    print('canceled task {!r}'.format(task))

    try:
        await task
    except asyncio.CancelledError:
        print('caught error from canceled task')
    else:
        print('task result: {!r}'.format(task.result()))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
```

当事件循环启动前取消 task 时，调用 `await task` 会抛出 `CanceledError`：

```
creating task
canceling task
canceled task <Task cancelling coro=<func_task() running at ...>>
caught error from canceled task
```

## 在 Coroutine 中创建 Task

`asyncio.ensure_future()` 函数返回一个与一个 coroutine 的执行相关联的 Task。这个 Task 实例可作为变量传入其他代码中，这样其他代码就可以直接 `await` 这个 Task 而不需要知道原始的 coroutine 是如何被创建的：

```py
# asyncio_ensure_future.py
import asyncio


async def wrapped():
    print('now in function wrapped')
    return 'result'


async def inner(task):
    print('now in function inner')
    print('inner: waiting for {!r}'.format(task))
    ret = await task
    print('inner: task return: {}'.format(ret))


async def outer():
    print('creating task')
    task = asyncio.ensure_future(wrapped())
    print('waiting for inner')
    await inner(task)
    print('inner returned')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(outer())
event_loop.close()
```

需要注意的是，传入 `ensure_future()` 的 coroutine 并不会马上启动，而是在某个地方使用 `await` 操作创建的 task 时它才会被执行。

```
creating task
waiting for inner
now in function inner
inner: waiting for <Task pending coro=<wrapped() running at ...>>
now in function wrapped
inner: task return: result
inner returned
```

# Future 对象

Future 对象表示一个还未完成的工作，时间循环可以监视 Future 对象的状态直至它变为 done

## 等待一个 Future 对象

```py
# asyncio_future_event_loop.py
import asyncio


def set_result(future, result):
    print('setting future result to {}'.format(result))
    future.set_result(result)


event_loop = asyncio.get_event_loop()
future = asyncio.Future()
print('scheduling set_result')
event_loop.call_soon(set_result, future, 'the result')
print('entering event loop')
ret = event_loop.run_until_complete(future)
print('returned result: {}'.format(ret))
event_loop.close()

print('future result: {}'.format(future.result()))
```

当调用 `set_result` 方法后，Future 对象的状态会被修改为 done，同时 `Future` 实例也会保存设置的结果值，供随后使用：

```
scheduling set_result
entering event loop
setting future result to the result
returned result: the result
future result: the result
```

Future 对象也可以同 await 关键字一起使用：

```py
# asyncio_future_await.py
import asyncio


def set_result(_future, _result):
    print('setting future result to {}'.format(_result))
    _future.set_result(_result)


async def main(loop):
    future = asyncio.Future()
    print('scheduling set_result')
    loop.call_soon(set_result, future, 'the result')
    ret = await future
    print('returned result: {}'.format(ret))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
event_loop.close()
```

await 会返回 Future 的结果：

```
scheduling set_result
setting future result to the result
returned result: the result
```

## Future 的回调函数

Future 在完成的时候可以执行一些回调函数，回调函数按注册时的顺序进行调用：

```py
# asyncio_future_callback.py
import asyncio
from asyncio import Future
import functools


def callback(_future, n):
    print('{}: future done: {}'.format(n, _future.result()))


async def register_callbacks(_future):
    """:type _future: Future"""
    print('registering callbacks on future')
    _future.add_done_callback(functools.partial(callback, n=1))
    _future.add_done_callback(functools.partial(callback, n=2))


async def main(_future):
    """:type _future: Future"""
    await register_callbacks(_future)
    print('setting result of future')
    _future.set_result('the result')


event_loop = asyncio.get_event_loop()
future = asyncio.Future()
event_loop.run_until_complete(main(future))
event_loop.close()
```

回调函数 `callback()` 的第一个参数是 Future 实例，要传递其他参数可以使用 `functools.partial()` 实现。

```
registering callbacks on future
setting result of future
1: future done: the result
2: future done: the result
```

# 控制组合式 Coroutines

对于线性执行的 Coroutines 可以很方便的通过 `await` 来控制。对于组合式的 Coroutines，比如在一个 coroutine 中等待其他并发执行的 coroutines 完成的操作也可以通过 asyncio 模块来实现。

## 等待多个 Coroutines

在一个 Coroutine 中等待其他多个 Coroutines 操作完成是一个很常见的需求，比如下载一批数据，执行对顺序没有要求，只想要最后的结果。

`wait()` 方法可以实现暂停当前 Coroutine，直到后台其他 Coroutines 操作完成：

```py
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
```

在 `wait` 内部，他使用一个集合来保存它创建的 Task 实例，所以它保存的 Task 的结果是无序的。`wait` 返回一个由两个集合组成的元组，一个保存状态为 done 的 Task，另一个保存状态为 pending 的 Task：

```
now in main
waiting for phases to complete
now in phase 2
now in phase 0
now in phase 1
done with phase 0
done with phase 1
done with phase 2
results: ['phase 2 result', 'phase 0 result', 'phase 1 result']
```

当调用 `wait` 时指定 timeout 参数才会有可能出现结果中包含状态为 pending 的 Task：

```py
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
```

对于 pending 的 Task 最好是把他们都 cancel 掉，否则事件循环在之后会继续执行它们或者退出程序时有警告信息。

```
now in main
wait 0.1s for phases to complete
now in phase 2
now in phase 0
now in phase 1
done with phase 0
1 completed and 2 pending
canceling tasks
exiting main
phase 1 canceled
phase 2 canceled
```

不 cancel 有警告的情况：

```py
# asyncio_wait_timeout_without_cancel.py
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
    print('exiting main')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(3))
event_loop.close()
```

运行结果：

```
now in main
wait 0.1s for phases to complete
now in phase 0
now in phase 1
now in phase 2
done with phase 0
1 completed and 2 pending
exiting main
done with phase 1
Task was destroyed but it is pending!
task: <Task pending coro=<phase() done, defined at ...> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x0000017B64AC0708>()]>>
```

pending 还会继续执行的情况：

```py
# asyncio_wait_timeout_without_cancel_continue.py
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
    print('exiting main')


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(3))
event_loop.run_until_complete(asyncio.sleep(3))
event_loop.close()
```

执行结果：

```
now in main
wait 0.1s for phases to complete
now in phase 0
now in phase 1
now in phase 2
done with phase 0
1 completed and 2 pending
exiting main
done with phase 1
done with phase 2
```

## 收集 Coroutine 结果

如果 Coroutines 是在程序中显式生成的，并且只关心返回值的话，`gather()` 是一种比较好的收集结果的方法：

```py
# asyncio_gather.py
import asyncio


async def phase1():
    print('now in phase 1')
    await asyncio.sleep(2)
    print('done with phase 1')
    return 'phase 1 result'


async def phase2():
    print('now in phase 2')
    await asyncio.sleep(1)
    print('done with phase 2')
    return 'phase 2 result'


async def main():
    print('now in main')
    print('waiting for phases to complete')
    results = await asyncio.gather(
        phase1(),
        phase2(),
    )
    print('results: {}'.format(results))


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.close()
```

通过 gather 方法创建的 task 对外部是不可见的，所以它们不能被取消，返回值是按输入参数顺序保存的对应 coroutine 的执行结果，无论真正执行的时候是否按顺序执行，最终的结果都是有序的：

```
now in main
waiting for phases to complete
now in phase 1
now in phase 2
done with phase 2
done with phase 1
results: ['phase 1 result', 'phase 2 result']
```

## 在后台操作完成时候做一些事情

`as_completed()` 是一个生成器，它将管理传入的 coroutines 的执行，每次迭代都将返回一个 coroutine 执行完成的 task。与 `wait` 一样，`as_completed` 也不会保证顺序。而跟 `wait` 的区别是它不会等待所有 coroutine 操作都完成后才能做其他操作。

```py
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
```

执行结果：

```
now in main
waiting for phases to complete
now in phase 2
now in phase 0
now in phase 1
done with phase 2
received answer phase 2 result
done with phase 1
received answer phase 1 result
done with phase 0
received answer phase 0 result
results: ['phase 2 result', 'phase 1 result', 'phase 0 result']
```
