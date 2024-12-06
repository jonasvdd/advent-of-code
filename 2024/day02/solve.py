from functional import seq
import numpy as np
import time


data = open("input").readlines()
# data = open("input_old").readlines()
split = " "
t0 = time.time()

# ----------------- shared --------------
data = (seq(data).map(lambda x: seq(x.split(split)).map(int).to_list())).to_pandas().values

# ----------------- part 1 --------------
deltas = np.diff(data, axis=1)

# check all deltas have the same sign
same_sign = np.sign(deltas) == np.sign(deltas[:, 0][:, None])
same_sign[np.isnan(deltas)] = True  # fill NaN with True (they are not relevant)
all_same_sign = np.all(same_sign, axis=1)

# check if all deltas have  difference between 1 and 3
min_delta = np.nanmin(np.abs(deltas), axis=1)
max_delta = np.nanmax(np.abs(deltas), axis=1)

valid = all_same_sign & (min_delta >= 1) & (max_delta <= 3)

sol1 = sum(valid)

t1 = time.time()
print("Part 1:", sol1)
print("Time:", round(t1 - t0, 4))


# ----------------- part 2 --------------
def check_safety(data: np.array, try_remove: bool = False) -> bool:
    data = data[~np.isnan(data)]

    deltas_ = np.diff(data)
    signs_ = np.sign(np.diff(data))
    all_same_sign_ = np.all(signs_ == signs_[0])
    if all_same_sign_:
        min_delta = np.nanmin(np.abs(deltas_))
        max_delta = np.nanmax(np.abs(deltas_))
        if min_delta >= 1 and max_delta <= 3:
            return True

    # try to remove each element and check if the new array is valid
    if not try_remove:
        return False
    for i in range(len(data)):
        if check_safety(np.delete(data, i), try_remove=False):
            return True

    return False


out = np.apply_along_axis(lambda x: check_safety(x, try_remove=True), -1, data)
sol2 = sum(out)
t2 = time.time()
print("Part 2:", sol2)
print("Time:", round(t2 - t0, 4))
