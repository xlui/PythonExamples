# 元类

类元编程是指在运行时创建或定制类的技艺。在 Python 中，类是一等对象，因此任何时候都可以使用函数创建新类，而无需使用 `class` 关键字。**类装饰器**也是函数，不过能够审查、修改，甚至把被装饰的类替换成其他类。最后，元类是类元编程最高级的工具：使用元类可以创建具有某种特质的全新类种，例如抽象基类。

元类功能强大，但是难以掌握。类装饰器能使用更简单的方式解决更多问题。其实，Python2.6 引入类装饰器后，元类很难使用真实的代码说明。

一个警告：除非开发框架，否则不要使用元类。

## 类工厂函数

我们首先从一个标准库种的函数来讲起。

`collections.namedtuple` 函数接收一个类名和几个属性名，创建一个 `tuple` 的子类并返回，其中的元素通过名称获取，还为调试提供了友好的字符串表示形式（`__repr__`）。

使用示例：

```
>>> from collections import namedtuple
>>> Dog = namedtuple('Dog', 'name weight owner')
>>> Dog
<class '__main__.Dog'>
>>> Dog.__mro__
(<class '__main__.Dog'>, <class 'tuple'>, <class 'object'>)
>>> rex = Dog('Rex', 30, 'Bob')
>>> rex
Dog(name='Rex', weight=30, owner='Bob')
>>> name, weight, _ = rex
>>> name, weight
('Rex', 30)
>>> rex.weight = 32
Traceback (most recent call last):
  ...
AttributeError: can't set attribute
```

我们将编写一个工厂函数 dog_factory，用于实现上面相同的功能，并且使对类实例的属性赋值可用。

dog_factory 函数的代码在下面：

```python
def dog_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__=field_names,
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)

    return type(cls_name, (object, ), cls_attrs)
```

导入 `dog_factory` 函数，将上面 Python Console 中的 `namedtuple` 替换成 `dog_factory`，结果依然一样，并且这次为 `rex.weight` 赋值不会出错。

通常来说，我们把 `type` 视为函数，因为我们像函数一样使用它，例如，调用 `type(my_object)` 获取对象所属的类——作用同 `my_object.__class__` 相同。然而 `type` 是一个类。被当做类使用时，传入三个参数可以新建一个类：

```python
type('Dog', (BaseClass, MixinClass), {'x':1, 'f': lambda self: self.x ** 2})
```

`type` 的三个参数分别是 `name`、`bases` 和 `dict`。最后一个参数是一个映射，指定新类的属性名和值。上述代码和下述代码作用相同：

```python
class Dog(BaseClass, MixinClass):
    x = 1

    def f(self):
        return self.x ** 2
```

`type` 的实例是类。把三个参数传给 `type` 是动态创建类动态创建类的常用方式。而 `collections.namedtuple` 采用了另一种方式，我们这里不做讨论，感兴趣可以自己去看源码。

## 类装饰器

类装饰器的参数是类，效果同普通装饰器一样。

```python
# 随手举例。
import collections


def entity(cls):
    for key, attr in cls.__dict__.items():
        if isinstance(attr, collections.MutableMapping):
            type_name = type(attr).__name__
            attr.storage_name = '{}#{}'.format(type_name, key)
    return cls
```

类装饰器有一个重大缺点：只对直接依附的类有效。这意味着，被装饰的类的子类可能继承也可能不继承装饰器所做的改动，具体情况视改动的方式而定。

## 导入时和运行时

为了正确的做元编程，你必须知道 Python 解释器什么时候计算各个代码块。Python 程序员会区分“导入时”和“运行时”，不过这两个术语没有严格的定义，而且二者之间存在灰色地带。在导入时，解释器会从上到下一次性解析完 .py 模块的源码，然后生成用于执行的字节码。如果句法有错误，就在此时报告。

编译是导入时的活动，不过那个时期还会做其他事情，因为 Python 中的语句几乎都是可执行的，也就是说语句可能会运行用户代码，修改用户程序的状态。尤其是 `import` 语句，它不只是声明，**在进程中首次导入模块时，还会运行导入模块中的全部顶层代码**。以后导入相同的模块则使用缓存，只做名称绑定。那些顶层代码可以做任何事情，包括通常在“运行时”做的事，例如连接数据库。因此，“导入时”和“运行时”之间的界线是模糊的：`import` 语句可以触发任何“运行时”行为。

导入模块时，解释器会执行顶层的 `def` 语句，解释器会编译函数的定义体（首次导入模块），把函数对象绑定到对应的全局名称上，但是显然解释器**不会执行函数的定义体**。通常这意味着解释器在导入时定义顶层函数，但是仅当在运行时调用函数才会执行函数的定义体。

对类来说，情况就不同了：在导入时，解释器会执行每个类的定义体，甚至会执行嵌套类的定义体。执行类定义体的结果是，**定义了类的属性和方法，并构建了类对象**。从这个意义上理解，类的定义体属于“顶层代码”，因为它在导入时运行。

对于上面的概念有一个理解即可，如果不是很清楚，可以去看 《流畅的Python》 第21章类元编程一章。

## 元类的基础知识

元类是制造类的工厂，不过不是函数，而是类。

根据 Python 的对象模型，类是对象，因此类肯定是另外某个类的实例。默认情况下，Python 中的类是 `type` 类的实例。也就是说，`type` 是大多数内置的类和用户定义的类的元类：

```python
>>> 'spam'.__class__
<class 'str'>
>>> str.__class__
<class 'type'>
>>> type.__class__
<class 'type'>
``` 

为了避免无限回溯，`type` 是其自身的实例。

关于 `object` 类和 `type` 类之间的关系：`object` 是 `type` 的实例，而 `type` 是 `object` 的子类。这种关系很神奇，无法用 Python 代码表述，因为定义其中一个之前另一个必须存在。 `type` 是自身实例这一点也很神奇。

除了 `type`，标准库中还有一些特别的元类，例如 ABCMeta 和 Enum。

若想理解元类，一定要知道这种关系：**元类（如 ABCMeta）从 `type` 类继承了构建类的能力**。

TODO: complete this
