from functional import seq
import numpy as np
import time
from tqdm.auto import tqdm

# data = open("input_old").readlines()
data = open("input").readlines()
t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
data = seq(data).map(lambda x: list(x.strip())).to_pandas().values
up, down, left, right = "^", "v", "<", ">"

turn_right_mapping = {up: right, right: down, down: left, left: up}
get_dirs = {up: (0, -1), down: (0, 1), left: (-1, 0), right: (1, 0)}


def facing_obstacle(d: np.ndarray, x: int, y: int, facing: str) -> bool:
    x_delta, y_delta = get_dirs[facing]
    y_ = min(max(0, y + y_delta), d.shape[0] - 1)
    x_ = min(max(0, x + x_delta), d.shape[1] - 1)
    return d[y_, x_] == "#"

def print_data(d: np.ndarray):
    for row in d:
        print("".join(row))


# ----------------- part 1 --------------
print_data(data)
visited_pt1 = data.copy()

y, x = np.array(np.where((data != ".") & (data != "#"))).ravel()
orientation = data[y, x]

outside_field = False
while not outside_field:
    if facing_obstacle(data, x, y, orientation):
        orientation = turn_right_mapping[orientation]
    else:
        visited_pt1[y, x] = "X"
        update_x, update_y = get_dirs[orientation]
        y, x = y + update_y, x + update_x

    outside_field = y < 0 or y >= data.shape[0] or x < 0 or x >= data.shape[1]

print()
print_data(visited_pt1)
print("Part 1:", np.sum(visited_pt1 == 'X'), "\t\tTime:", round(time.time() - t0, 4))

# ----------------- part 2 --------------
def check_in_loop(d: np.ndarray ) -> bool:
    visited = d.copy()
    prev_orientations: dict = {}  # store all orientations for each point (so we can check if we are in a loop)

    y, x = np.array(np.where((d != ".") & (d != "#"))).ravel()
    orientation = d[y, x]
    def add_orientation(y, x, orientation):
        if (y, x) not in prev_orientations:
            prev_orientations[(y, x)] = {orientation}
        else:
            prev_orientations[(y, x)].add(orientation)

    outside_field = False
    while not outside_field:
        if facing_obstacle(d, x, y, orientation):
            orientation = turn_right_mapping[orientation]
        else:
            visited[y, x] = "X"
            update_x, update_y = get_dirs[orientation]
            y, x = y + update_y, x + update_x

        if orientation in prev_orientations.get((y, x), {}):
            return True
        add_orientation(y, x, orientation)

        outside_field = y < 0 or y >= data.shape[0] or x < 0 or x >= data.shape[1]

    # went out of the field
    return False



y, x = np.array(np.where((data != ".") & (data != "#"))).ravel()
orientation = data[y, x]

initial_line_of_sight = np.zeros(data.shape)
initial_line_of_sight[y, x] = 1
faced_obstacle = False
while not faced_obstacle:
    if facing_obstacle(data, x, y, orientation):
        faced_obstacle = True
    else:
        update_x, update_y = get_dirs[orientation]
        y, x = y + update_y, x + update_x
    initial_line_of_sight[y, x] = 1


total_loops = 0
# dit kan veel optimaler -> door een mask bij te houden van orientations die tot loops leiden
# (maar die niet op het pad van de (inserted) obstacles liggen)
for y, x in tqdm(np.argwhere(visited_pt1 == "X")):
    if initial_line_of_sight[y, x]:  # check if in initial line_of_sight
        continue
    d_obstacle = data.copy()
    d_obstacle[y, x] = "#" # add obstacle
    total_loops += check_in_loop(d_obstacle)

print("Part 2:", total_loops, "\t\tTime:", round(time.time() - t0, 4))
