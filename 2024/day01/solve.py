from functional import seq
import numpy as np
import time


data = open("input").readlines()
# data = open("input_test").readlines()
t0 = time.time()

# ----------------- shared --------------
# TODO -> try to use polars ...
data = (seq(data).map(lambda x: seq(x.split("  ")).map(int).to_list())).to_pandas().values
left, right = data[:, 0], data[:, 1]

# ----------------- part 1 --------------
sol1 = np.sum(np.abs(np.sort(left) - np.sort(right)))
t1 = time.time()
print("Part 1:", sol1)
print("Time:", round(t1 - t0, 4))


# ----------------- part 2 --------------
# expand the dimensions (and then sum the matches)
appearances_in_right = (left[:, None] == right[None, :]).sum(axis=1)
sol2 = np.sum(left * appearances_in_right)
t2 = time.time()
print("Part 2:", sol2)
print("Time:", round(t2 - t0, 4))
