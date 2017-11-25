# dis

dis — Disassembler for Python bytecode，即把 Python 代码反汇编为字节码指令。

可以通过这种方式进行代码分析。

<br>

示例：

```bash
# 命令调用
python -m dis xxx.py
```

```python
# 代码中使用
import dis
def fn_terse(func=sum, upper=1000000):
    return func(range(upper))

if __name__ == '__main__':
    dis.dis(fn_terse)
```
