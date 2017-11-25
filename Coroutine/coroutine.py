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
