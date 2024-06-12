a = {1: 2, 3: 4}
print(sum([int(i+1) for i in filter(lambda x: x in [1], a)]))