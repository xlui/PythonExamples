# Built-in Functions

> map  
> filter  
> sorted

## map

函数原型:

```python
map(function, iterable, ...)
```

将 function 施加到 iterable 的每一个元素，并返回一个 generator。

代码示例：

```python
>>> map(str, [i for i in range(10)])
<map object at 0x0000027D40CBAE80>
>>> list(map(str, [i for i in range(10)]))
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
>>> map(lambda x: x**2, [i for i in range(10)])
<map object at 0x0000027D40CBAC18>
```

## filter

函数原型：

```python
filter(function, iterable)
```

用 function 过滤 iterable，function 返回 true 保留，返回 false 去掉，最终返回一个 generator。

代码示例：

```python
>>> filter(lambda x: x % 2, [1, 2, 4, 5, 6, 9, 10, 15])
<filter object at 0x0000027D40CBAE80>
>>> list(filter(lambda x: x % 2, [1, 2, 4, 5, 6, 9, 10, 15]))
[1, 5, 9, 15]
>>> filter(lambda s: s and s.strip(), ['A', '', 'B', None, 'C', '  '])
<filter object at 0x0000027D40CC4C18>
```

## sorted

函数原型：

```python
sorted(iterable, *, key=None, reverse=False)
```

对一个 iterable 序列进行排序。  
key 指定的函数将作用于序列的每一个元素上，并根据 key 函数返回的结果进行排序。  
reverse 决定正向还是反向排序。  

代买示例：

```python
>>> list_for_sort = [36, 5, -12, 9, -21]
>>> sorted(list_for_sort)
[-21, -12, 5, 9, 36]
>>> sorted(list_for_sort, key=abs)
[5, 9, -12, -21, 36]
>>> sorted(list_for_sort, key=abs, reverse=True)
[36, -21, -12, 9, 5]

>>> str_for_sort = ['bob', 'about', 'Zoo', 'Credit']
>>> sorted(str_for_sort)
['Credit', 'Zoo', 'about', 'bob']
>>> sorted(str_for_sort, key=str.lower)
['about', 'bob', 'Credit', 'Zoo']
>>> sorted(str_for_sort, key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']
```
