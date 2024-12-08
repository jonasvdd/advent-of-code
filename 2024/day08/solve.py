from functional import seq
import numpy as np
import time
import itertools

# data = open("input_old").readlines()
data = open("input").readlines()

t0 = time.time()  # data I/O doesn't count in the time

# ----------------- shared --------------
data = seq(data).map(str.strip).map(list).to_pandas().values


def print_data(d: np.ndarray):
    print("\n".join(["".join(row) for row in d.astype(str)]))


def check_in_bounds(d: np.ndarray, y, x):
    return 0 <= y < d.shape[0] and 0 <= x < d.shape[1]


# ----------------- part 1 --------------
# print_data(data)
antinode_locations = np.zeros(data.shape, dtype=bool)
for antenna_type in set(np.unique(data)).difference("."):
    antenna_locs = np.argwhere(data == antenna_type)
    for (a1_y, a1_x), (a2_y, a2_x) in list(itertools.combinations(antenna_locs, 2)):
        dx = a2_x - a1_x
        dy = a2_y - a1_y

        an1_x, an1_y = a1_x - dx, a1_y - dy
        if check_in_bounds(data, an1_y, an1_x):
            antinode_locations[an1_y, an1_x] = True

        an2_x, an2_y = a2_x + dx, a2_y + dy
        if check_in_bounds(data, an2_y, an2_x):
            antinode_locations[an2_y, an2_x] = True

# print_data(antinode_locations.astype(int))
print("Part 1:", np.sum(antinode_locations), "\t\tTime:", round(time.time() - t0, 4))

# ----------------- part 2 --------------
# antinode_locations = np.zeros(data.shape, dtype=bool)
antinode_locations = np.zeros(data.shape, dtype=bool)
for antenna_type in set(np.unique(data)).difference("."):
    antenna_locs = np.argwhere(data == antenna_type)
    for (a1_y, a1_x), (a2_y, a2_x) in list(itertools.combinations(antenna_locs, 2)):
        dx, dy = a2_x - a1_x, a2_y - a1_y

        # harmonic 0 -> same location
        an1_x, an1_y = a1_x, a1_y
        while check_in_bounds(data, an1_y, an1_x):
            antinode_locations[an1_y, an1_x] = True
            an1_x -= dx
            an1_y -= dy

        an2_x, an2_y = a2_x, a2_y
        while check_in_bounds(data, an2_y, an2_x):
            antinode_locations[an2_y, an2_x] = True
            an2_x += dx
            an2_y += dy

# print_data(np.where(antinode_locations, "#", "."))
print("Part 1:", np.sum(antinode_locations), "\t\tTime:", round(time.time() - t0, 4))