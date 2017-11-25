import time
import tqdm

# 以下两段代码作用相同
# for _ in tqdm.tqdm(range(1000)):
#     time.sleep(.01)

# for _ in tqdm.trange(1000):
#     time.sleep(.01)

# 传入字符列表
# l_char = tqdm.tqdm(['a', 'b', 'c', 'd'])
# for char in l_char:
#     l_char.set_description("Processing {}".format(char))
#     time.sleep(.5)
# l_char.close()

# # 手动控制更新
pbar = tqdm.tqdm(total=100)
for i in range(10):
    pbar.update(10)
    time.sleep(1)
pbar.close()
