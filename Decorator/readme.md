# Decorator

在 Python 中函数也是对象，而且函数对象可以被赋值给变量，所以，通过变量也能调用该函数。

本质上， Decorator 就是一个返回函数的高阶函数。

## 示例：

```python
def log(func):
    def wrapper(*args, **kw):
        print('call %s()' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    pass

if __name__=='__main__':
    now()
```

上述代码中将 `@log` 放到 `now()` 函数前相当于执行了语句：

```python
now = log(now)
```

现在调用 `now()` 函数：
```bash
python example.py
# call now()
```

## 用装饰器计算函数运行时间

```py
from time import time
from functools import wraps


def time_func(func):
    @wraps(func)
    def measure_time(*args, **kwargs):
        time_start = time()
        result = func(*args, **kwargs)
        time_stop = time()
        print('@time_func: function [{}] takes {} seconds.'.format(func.__name__, time_stop - time_start))
        return result
    return measure_time
```

通过在需要测量的函数前 `@time_func` 即可在函数运行结束后看到运行时间。
