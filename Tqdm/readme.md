# tqdm 模块

Tqdm 是一个快速，可扩展的Python进度条模块。可以在 Python 长循环中添加一个进度提示信息，用户只需要封装任意的可迭代对象 tqdm(iterator)。

![tqdm](./tqdm.gif)

## 简单的显示进度条

```python
for _ in tqdm.tqdm(range(1000)):
    time.sleep(.01)
```

## tqdm.trange(n) = tqdm.tqdm(range(n))

```python
for _ in tqdm.trange(1000):
    time.sleep(.01)
```

## 传入列表

```python
l_char = tqdm.tqdm(['a', 'b', 'c', 'd'])
for char in l_char:
    l_char.set_description("Processing {}".format(char))
    time.sleep(.5)
l_char.close()
```

## 手动控制更新

```python
pbar = tqdm.tqdm(total=100)
for i in range(10):
    pbar.update(10)
    time.sleep(1)
pbar.close()
```
