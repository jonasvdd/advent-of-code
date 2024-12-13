import numpy as np
import time
import scipy.linalg
from tqdm.auto import tqdm
from typing import List, Tuple
from itertools import product
import scipy

# data = open("input_old").readlines()
data = open("input").readlines()
dxs_a, dys_a, dxs_b, dys_b, targets_x, targets_y = [], [], [], [], [], []

for row in data:
    row = row.strip()
    if not len(row):
        continue
    right = row.split(": ")[-1].split(", ")

    if "Button" in row:
        dx, dy = right[0].lstrip("X+"), right[1].lstrip("Y+")
        if "A:" in row:
            dxs_a.append(int(dx))
            dys_a.append(int(dy))
        else:
            dxs_b.append(int(dx))
            dys_b.append(int(dy))
    elif "Prize" in row:
        targets_x.append(int(right[0].lstrip("X=")))
        targets_y.append(int(right[1].lstrip("Y=")))

t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
cost_A = 3
cost_B = 1


def find_combinations_target(d1, d2, target) -> List[Tuple]:
    mx, mn = max(d1, d2), min(d1, d2)

    # mx * x + mn * y = target
    # y = (target - mx * x) / mn
    sol = []
    for i in range(target // mx + 1):
        mn_y = (target - mx * i) / mn
        if mn_y.is_integer():
            sol.append([i, int(mn_y)])

    if len(sol) == 0:
        return []

    sol = np.asarray(sol)
    if mx == d2:
        sol = sol[:, ::-1]
    return list(map(tuple, sol))


# ----------------- part 1  ---------------
tot_tokens = 0
for i, (target_x, target_y) in enumerate(zip(targets_x, targets_y)):
    dxa, dxb, dya, dyb = dxs_a[i], dxs_b[i], dys_a[i], dys_b[i]
    possible_combs_x = find_combinations_target(dxa, dxb, target_x)
    possible_combs_y = find_combinations_target(dya, dyb, target_y)
    possible_combs = set(possible_combs_x).intersection(possible_combs_y)
    if not len(possible_combs):
        continue

    possible_combs = np.array([list(comb) for comb in possible_combs])
    prize = possible_combs[:, 0] * cost_A + possible_combs[:, 1] * cost_B
    tot_tokens += np.min(prize) if len(prize) else -1

print("Part 1:", tot_tokens, "Time:", time.time() - t0)


# ----------------- part 2 ---------------
def get_numpy_int_mask(arr: np.array) -> np.array:
    mask = np.ones(arr.shape)
    np.mod(arr, 1, out=mask)
    return mask == 0


def find_combinations_target_linalg(dx_a, dx_b, targetx, dy_a, dy_b, targety):
    # fmt: off
    A = np.array([[dx_a, dx_b],
                  [dy_a, dy_b]]
    )
    b = np.array([targetx, targety])

    det = np.linalg.det(A)
    if det == 0: # no solution or infinite solutions
        return []

    solution = scipy.linalg.solve(A, b)  # , assume_a='pos')
    if not all(get_numpy_int_mask(np.round(solution, 3))):
        return []
    return [np.round(solution)]

tot_tokens = 0
for i, (target_x, target_y) in enumerate(zip(targets_x, targets_y)):
    target_x += 10000000000000
    target_y += 10000000000000
    possible_combs = find_combinations_target_linalg(
        dxs_a[i], dxs_b[i], target_x, dys_a[i], dys_b[i], target_y
    )
    if not len(possible_combs):
        continue

    tot_tokens += possible_combs[0][0] * cost_A + possible_combs[0][1] * cost_B

print("Part 2:", int(tot_tokens), "Time:", time.time() - t0)
