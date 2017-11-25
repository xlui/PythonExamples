import collections

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
