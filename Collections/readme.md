# collections

> namedtuple  
> deque  
> defaultdict

## namedtuple

collections.namedtuple 是一个工厂函数，它可以用来**构建一个带字段名的元组和一个有名字的类** -- 这个带名字的类对调试程序有很大帮助

用 namedtuple 构建的类的实例消耗的内存与元组是一样的。这个实例跟普通的对象实例比起来也要小一点，因为 Python 不会使用 `__dict__` 来存放这些实例的属性。

示例：
```python
>>> import collections
>>> Point = collections.namedtuple('Point', 'x y')
>>> point = Point(1, 2)
>>> print('_fields of namedtuple:', Point._fields)
_fields of namedtuple: ('x', 'y')
>>> type(point)
<class '__main__.Point'>
>>> point.x, point.y
(1, 2)
``` 

## deque

列表有 `.append` 和 `.pop` 方法，可以作为栈或者队列来用。但是删除列表的第一个元素（或者在列表的第一个元素之前添加一个元素）之类的操作十分耗时。 

collections.deque（双向队列） 是一个**线程安全、可以快速从两端添加或者删除元素**的数据类型。

双向队列实现了大部分列表所拥有的方法，也有一些额外的符合自身设计的方法。但是为了实现这些方法，双向队列也付出了一些代价，例如从队列中间删除元素的操作会慢一点，因为它只对在头尾的操作进行了优化。

示例：
```python
>>> from collections import deque
>>> dq = deque(range(10), maxlen=10)
>>> dq
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.rotate(3)    # 队列旋转，参数大于 0 时队列会像链子一样顺时针旋转 n 个位置
>>> dq
deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
>>> dq.rotate(-4)
>>> dq
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
>>> dq.appendleft(-1)
>>> dq
deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.extend([11, 22, 33])
>>> dq
deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)
>>> dq.extendleft([10, 20, 30, 40])
>>> dq
deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
```

## defaultdict

在用户创建 defaultdict 对象的时候，需要给他配置一个为找不到的键创建默认值的方法。

具体而言，在实例化一个 defaultdict 的时候，需要给构造方法提供一个可调用对象，这个可调用对象会在 `__getitem__` 碰到找不到的键的时候被调用，让 `__getitem__` 返回某种默认值。

示例：
```python
dict_test = {}
dict_test_default = collections.defaultdict(list)
for i in range(10):
    for j in range(5):
        # below 3 lines code, makes at least 2 querys
        value = dict_test.get(i, [])
        value.append(j)
        dict_test[i] = value
        # below 1 line code, makes 1 query
        dict_test_default[i].append(j)

for key, value in dict_test.items():
    print(key, value)
for key, value in dict_test_default.items():
    print(key, value)
```