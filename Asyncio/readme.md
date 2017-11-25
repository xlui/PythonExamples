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
