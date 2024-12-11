from functional import seq
import numpy as np
import time

# data = open("input_test2").readlines()
# data = open("input_old").readlines()
data = open("input").readlines()
from typing import NamedTuple

t0 = time.time()  # data I/O doesn't count in the time

# ----------------- shared --------------
data = np.array([[int(x.replace(".", "-1")) for x in line.strip()] for line in data])
delta_y_x = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])  # left  # right  # up  # down


def print_data(d: np.array):
    for row in d.astype(str):
        print("".join(row))
    # print("".join(np.where(d_ == str(FREE_SPACE_VAL), ".", d_)))


def on_map(d: np.array, y: int, x: int) -> bool:
    return 0 <= y < d.shape[0] and 0 <= x < d.shape[1]


# ----------------- part 1 ---------------
def find_increasing_neighbors_vect(d: np.ndarray, current_yxs: np.array) -> np.array:
    if len(current_yxs) == 0:
        return []
    # print("current_yxs\n", current_yxs)
    cur_vals = d[tuple(current_yxs.T)]
    # print("cur_vals\n", cur_vals)
    assert all(cur_vals == cur_vals[0])
    next_val = cur_vals[0] + 1

    # print("current_yxs:\n", current_yxs)
    possible_next_locs = (current_yxs + delta_y_x[:, None, :]).reshape(-1, 2)
    # print("possible_next_locs\n", possible_next_locs)

    # verify if on map
    valid_location_mask = (
        np.all(possible_next_locs >= 0, axis=1)
        & (possible_next_locs[:, 0] < d.shape[0])
        & (possible_next_locs[:, 1] < d.shape[1])
    )
    possible_next_locs = possible_next_locs[valid_location_mask]
    possible_next_vals = data[tuple(possible_next_locs.T)]

    valid_value_mask = possible_next_vals == next_val

    current_yxs_exp = np.repeat(current_yxs[None, :, :], 4, axis=0).reshape(-1, 2)
    # print("current_yxs_exp\n", current_yxs_exp)

    return (
        current_yxs_exp[valid_location_mask][valid_value_mask],
        possible_next_locs[valid_value_mask],
    )


positions = np.argwhere(data == 0)
path = [[(*sp.tolist(),)] for sp in positions]

for i in range(9):
    prev_positions, next_positions = find_increasing_neighbors_vect(data, positions)
    # convert to list of tuples
    prev_positions = [(*pp.tolist(),) for pp in prev_positions]
    next_positions = [(*np.tolist(),) for np in next_positions]

    new_path = []
    for prev_pos, next_pos in zip(prev_positions, next_positions):
        for p in path:
            if p[-1] == prev_pos:
                new_path.append([*p, next_pos])

    path = new_path
    positions = np.unique(np.array([list(p[-1]) for p in new_path]), axis=0)
    # print(f"path {i} --> {i+1}")
    # print("prev_positions", prev_positions)
    # print("next_positions", next_positions)
    # for p in path:
    # print("\t", p)

# for the first part we need to find the unique trailheads
trailhead_list = np.array([p[0] + p[-1] for p in path])

print("part 1", len(np.unique(trailhead_list, axis=0)))

# for part two, we need to know sum of the number of paths that end at each trailhead
print("part 2", len(path))
