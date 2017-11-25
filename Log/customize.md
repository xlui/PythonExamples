## 自定义日志类

利用变量重命名与鸭子类型，我们可以手动定义一个日志类（logger），这个类的作用是替代默认的 sys.stdout 的值，在输出到 stdout 的同时输出到文件，让我们可以使用 `print()` 来输出信息到文件

```python
import sys

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)        # 正常输出到 stdout
        self.log.write(message)             # 同时写入文件

    def flush(self):
        pass

    def close(self):
        self.log.close()

if __name__ == '__main__':
    sys.stdout = Logger()
    print("Hello World")
    sys.stdout.close()
```

使用的时候只需要将 sys.stdout 的值设置为 `Logger` 类的实例即可。
