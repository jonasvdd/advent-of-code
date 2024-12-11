from itertools import chain
import time
from typing import Dict, List

data = open("input").readlines()[0].strip()
# data = open("input_old").readlines()[0].strip()

t0 = time.time()  # data I/O doesn't count in the time

# ----------------- shared --------------
data = [int(x) for x in data.split(" ")]
print(data)


def update_stone(s_val: int):
    if s_val == 0:
        return [1]
    elif len(str(s_val)) % 2 == 0:
        offset = len(str(s_val)) // 2
        return [int(str(s_val)[:offset]), int(str(s_val)[offset:])]
    else:
        return [s_val * 2024]


# ----------------- part 1 ---------------
data_ = data.copy()
for id in range(25):
    data_ = list(chain.from_iterable(list(map(update_stone, data_))))

print("Part 1:", len(data_), "\t\tTime:", round(time.time() - t0, 4))

# ----------------- part 2 ---------------
# No time for brute force -> let's introduce some caching :)
stone_cache: Dict[int, List[int]] = {}
stone_count: Dict[int, int] = {}
for d in data:
    stone_count[d] = stone_count.get(d, 0) + 1

for id in range(75):
    new_stone_count = {}
    for cur_stone, count in stone_count.items():
        # add the stone to the cache
        if cur_stone not in stone_cache:
            stone_cache[cur_stone] = update_stone(cur_stone)

        for new_stone in stone_cache[cur_stone]:
            new_stone_count[new_stone] = new_stone_count.get(new_stone, 0) + count

    stone_count = new_stone_count

print("Part 2:", sum(stone_count.values()), "\t\tTime:", round(time.time() - t0, 4))
