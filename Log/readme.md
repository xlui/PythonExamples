# 日志模块

Python的 logging 模块提供了通用的日志系统，可以方便第三方模块或者是应用使用。这个模块提供不同的日志级别，并可以采用不同的方式记录日志，比如文件，HTTP GET/POST，SMTP，Socket等，甚至可以自己实现具体的日志记录方式。

模块提供 logger，handler，filter，formatter。

- logger：提供日志接口，供应用代码使用。logger 最常用的操作有两类：配置和发送日志消息。可以通过 `logging.getLogger(name)` 获取 logger 对象，如果不指定 name 则返回 root 对象，多次使用相同的 name 调用 getLogger 方法返回同一个 logger 对象。
- handler：将日志记录（log record）发送到合适的目的地（destination），比如文件，socket等。一个 logger 对象可以通过 addHandler 方法添加 0 到多个 handler，每个 handler 又可以定义不同日志级别，以实现日志分级过滤显示。
- filter：提供一种优雅的方式决定一个日志记录是否发送到 handler。
- formatter：指定日志记录输出的具体格式。formatter 的构造方法需要两个参数：消息的格式字符串和日期字符串，这两个参数都是可选的。

logger，handler 和日志消息的调用可以有具体的日志级别（Level），只有在日志消息的级别大于 logger 和 handler 的级别。默认的级别顺序：DEBUG < INFO < WARNING < ERROR < CRITICAL。

## 1. 默认的日志信息只输出到 stdout

```python
import logging

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
```

输出：

```
WARNING:root:warning message
ERROR:root:error message
CRITICAL:root:critical message
```

默认的日志级别是 WARNING

## 2. 定制输出格式

方式一：直接配置

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,                # 设置日志级别，只有高于设置级别的日记会被记录
    format='%(asctime)s [file: %(filename)s] [line: %(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',    # 设置日期输出格式，必须现在 format 中设置日期输出，否则无效
    filename='logging.log',             # 如果设置了 filename，日志就会被输出到文件而不是标准输出
    filemode='w',                       # 写入日志到文件的模式
)

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')
```

方法二：使用 Handler 和 Formatter 进行更细致的配置

```python
import logging.handlers

log_file = 'test.log'

handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('testLogger')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
```

会在当前文件夹下产生一个 test.log 文件

```
2017-11-04 22:08:52,348 - t.py:15 - testLogger - debug message
2017-11-04 22:08:52,348 - t.py:16 - testLogger - info message
2017-11-04 22:08:52,348 - t.py:17 - testLogger - warning message
2017-11-04 22:08:52,348 - t.py:18 - testLogger - error message
2017-11-04 22:08:52,348 - t.py:19 - testLogger - critical message
```

代码应该很简单易懂，handler 设置日志记录的属性，包括保存形式等，Formatter 设置日志记录的格式。

关于 formatter 的配置，采用的是 `%(<dict key>)s` 的形式，就是字典关键字替换。替换的关键字包括：

Format|Description
:---:|:---:
%(name)s|logger 名字
%(levelno)s|日志等级（DEBUG, INFO, WARNING, ERROR, CRITICAL），数字表示
%(levelname)s|日志等级（DEBUG, INFO, WARNING, ERROR, CRITICAL），字符串表示
%(pathname)s|调用 logging 的语句所在文件的绝对路径
%(filename)s|pathname 中的文件名部分
%(module)s|模块
%(funcName)s|包含调用 logging 语句的函数
%(lineno)s|调用 logging 语句的行
%(created)f|logging 语句创建的时间（time.time())
%(acstime)s|对人友好的时间形式
%(msesc)d|微秒
%(thread)d|线程 ID（如果存在）
%(threadName)s|线程名（如果存在）
%(process)d|进程名（如果存在）
%(message)s|日志信息

更多信息可以参考官网。

## 3. 从外部文件导入配置

logging 支持从外部文件中导入配置。

配置文件 test.conf：

```
[loggers]
keys=root, simpleExample

[handlers]
keys=consoleHandler, fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=fileHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('a.log',)

[formatter_simpleFormatter]
format=%(asctime)s [file: %(filename)s] [line: %(lineno)d] [%(levelname)s] %(message)s
datefmt=%a, %d %b %Y %H:%M:%S
```

测试：

```python
import logging.config

logging.config.fileConfig('test.conf')

logger = logging.getLogger('simpleExample')

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')
```

对于配置文件 logging 采用模式匹配的方式进行配置，正则表达式为 `r'^[(.*)]$'`，从而匹配出所有组件。对于同一个组件中多个实例的情况使用逗号进行分隔。对于一个实例的配置则采用 `componentName_instanceName` 配置块。使用这种方式还是很简单的。

对于多模块使用 logging 这里不作说明，如果有需求可以去看官方文档。
