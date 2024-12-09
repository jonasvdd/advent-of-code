import numpy as np
import time

# data = open("input_old").readlines()[0].strip()
data = open("input").readlines()[0].strip()

t0 = time.time()  # data I/O doesn't count in the time

# ----------------- shared --------------
data = np.array([int(x) for x in data])
file_spaces = data[0::2]
free_spaces = data[1::2]
assert len(file_spaces) >= len(free_spaces)

FREE_SPACE_VAL = -1


def print_data(d: np.array):
    d_ = d.copy().astype(str)
    print("".join(np.where(d_ == str(FREE_SPACE_VAL), ".", d_)))


# first, expand the data
data_exp = []
for id in range(len(file_spaces)):
    file_spc = file_spaces[id]
    data_exp.extend([id] * file_spc)

    # there can be more files than free spaces
    if id <= len(free_spaces) - 1:
        free_spc = free_spaces[id]
        data_exp.extend([FREE_SPACE_VAL] * free_spc)
data_exp = np.array(data_exp)
# print_data(np.asarray(data_exp))


# ----------------- part 1 ---------------
def all_free_space_at_the_end(d_exp: np.array) -> bool:
    where_mask = np.where(d_exp == FREE_SPACE_VAL)[0]
    if len(where_mask) == 0:
        return False

    where_mask -= len(d_exp) - 1
    return where_mask[-1] == 0 and np.all(np.diff(where_mask) == 1)


d_exp_mv = np.copy(data_exp)
free_space_idxs = np.where(d_exp_mv == FREE_SPACE_VAL)[0]
value_idxs = np.where(d_exp_mv != FREE_SPACE_VAL)[0]

i = 0
while not all_free_space_at_the_end(d_exp_mv):
    # swap the free space and value
    d_exp_mv[free_space_idxs[i]] = d_exp_mv[value_idxs[-(i + 1)]]
    d_exp_mv[value_idxs[-(i + 1)]] = FREE_SPACE_VAL
    i += 1


file_mask = d_exp_mv != FREE_SPACE_VAL
checksum = np.sum(d_exp_mv[file_mask] * np.arange(d_exp_mv.shape[0])[file_mask])
print("Part 1:", checksum, "\t\tTime:", round(time.time() - t0, 4))


# ----------------- part 2 --------------
print("-" * 50)
d_exp_mv2 = np.copy(data_exp)

free_spaces_cp = free_spaces.copy()
free_space_deltas = np.zeros(free_spaces.shape[0], dtype=int)
free_spaces_cum = np.cumsum(free_spaces)
file_spaces_cum = np.cumsum(file_spaces)
print_data(d_exp_mv2)

for idx in range(1, len(file_spaces)):
    # get the size of the files (starting from the end)
    f_size = file_spaces[-idx]
    end_loc = file_spaces_cum[-idx] + free_spaces_cum[-idx]
    start_loc = end_loc - f_size
    f_val = data_exp[start_loc]

    available_loc = np.where(free_spaces_cp >= f_size)[0]
    if len(available_loc):
        swp_idx = available_loc[0]

        swp_start = (
            file_spaces_cum[swp_idx]
            + free_spaces_cum[swp_idx]
            + free_space_deltas[swp_idx]
            - free_spaces[swp_idx]
        )
        swp_end = swp_start + f_size

        if swp_start > start_loc:
            continue

        d_exp_mv2[swp_start:swp_end] = f_val
        d_exp_mv2[start_loc:end_loc] = FREE_SPACE_VAL
        free_spaces_cp[swp_idx] -= f_size
        free_space_deltas[swp_idx] += f_size

        # print_data(d_exp_mv2)


file_mask = d_exp_mv2 != FREE_SPACE_VAL
checksum = np.sum(d_exp_mv2[file_mask] * np.arange(d_exp_mv.shape[0])[file_mask])
print("Part 2:", checksum, "\t\tTime:", round(time.time() - t0, 4))
