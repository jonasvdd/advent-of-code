from functional import seq
import numpy as np
import time
from tqdm.auto import tqdm

# data = open("input_old").readlines()
data = open("input").readlines()
data: np.ndarray = seq(data).map(lambda x: list(x.strip())).to_pandas().values

t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
# perimeter = number of sides that do not touch a garden plot of the same region
def print_data(d: np.ndarray):
    for row in d:
        print("".join(row))


def compute_number_of_sides(area_mask: np.ndarray) -> int:
    # print('single area')
    # print_data(area_mask.astype(int).astype(str))

    nb_edges = 0
    for shift, axis in [(1, 0), (-1, 0), (1, 1), (-1, 1)]:
        # compute all the left, right, upper, lower edges
        edge_mask = area_mask & ~np.roll(area_mask, shift, axis=axis)
        if axis == 0:
            slc = np.index_exp[:1, :] if shift == 1 else np.index_exp[-1:, :]
        else:
            slc = np.index_exp[:, :1] if shift == 1 else np.index_exp[:, -1:]
        edge_mask[slc] = area_mask[slc]  # fix the edges at the border

        # print(f"shift: {shift}, axis: {axis}")
        # print_data(edge_mask.astype(int).astype(str))

        # nifty trick with np.diff and where to find the "positive" edges
        diff = np.where(np.diff(edge_mask, axis=1 - axis, prepend=0) == 1, 1, 0)
        # print("diff")
        # print_data(diff.astype(int).astype(str))

        nb_edges += np.sum(diff)

    return nb_edges


# ----------------- part 1 & 2 ---------------
# print_data(data)
total_fence_price, total_fence_price_bulk = 0, 0

# Fence price = perimeter * area
for plant_type in tqdm(np.unique(data)):
    plant_type_mask = data == plant_type
    pair_set_list = []

    perimeter = plant_type_mask * 4  # by default the perimeter is 4
    for shift, axis in [(1, 0), (-1, 0), (1, 1), (-1, 1)]:
        neighbor = np.roll(plant_type_mask, shift, axis=axis)

        # print(f"plant type: {plant_type} -> neighbor {shift}, {axis}")
        # print_data(neighbor.astype(int).astype(str))

        if axis == 0:
            slc = np.index_exp[:1, :] if shift == 1 else np.index_exp[-1:, :]
        else:
            slc = np.index_exp[:, :1] if shift == 1 else np.index_exp[:, -1:]
        neighbor[slc] = False  # set the rolled part to False

        neighbor_1 = np.argwhere(neighbor & plant_type_mask)
        offset = np.array([-shift, 0]) if axis == 0 else np.array([0, -shift])
        neighbor_2 = neighbor_1 + offset

        # a lot of logic to find the areas
        for n1, n2 in zip(neighbor_1, neighbor_2):
            n1, n2 = (*n1.tolist(),), (*n2.tolist(),)

            added = False
            for s in pair_set_list:
                if n1 in s or n2 in s:
                    s.update({n1, n2})
                    added = True
                    break
            if not added:
                pair_set_list.append({n1, n2})

        perimeter -= neighbor

        # merge the connected areas (i.e. prune the list to larger areas)
        reduced_set_list = [pair_set_list[0]]
        for s_ in pair_set_list[1:]:
            added_ = False
            for item in reduced_set_list:
                if s_ & item:
                    item.update(s_)
                    added_ = True
                    break
            if not added_:
                reduced_set_list.append(s_)

        pair_set_list = reduced_set_list

    # apply the mask to the perimeter
    perimeter = plant_type_mask * perimeter

    # print("plant type:", plant_type, "plant type mask")
    # print_data(plant_type_mask.astype(int).astype(str))
    # print("perimeter values")
    # print_data(perimeter.astype(int).astype(str))

    # ------ compute the fence price (part 1 & 2) ------
    # first add the standalone areas
    fence_price_plant = np.sum(perimeter == 4) * 4

    # for the bulk price (standalone still have 4 sides) -> so same as default price
    fence_price_plant_bulk = fence_price_plant

    # then add the areas that are connected
    for s in pair_set_list:
        s = np.array([list(l) for l in s])
        area = len(s)

        # Part 1: use the sum of the perimeter
        perimeter_sum = perimeter[tuple(s.T)].sum()
        # print(f"connected areas -> fence price: {area} * {perimeter_sum} = {area * perimeter_sum}")
        fence_price_plant += perimeter_sum * area

        # Part 2: use the total number of sides
        single_area = np.zeros_like(perimeter, dtype=bool)
        single_area[tuple(s.T)] = True
        number_of_sides = compute_number_of_sides(single_area)
        fence_price_plant_bulk += number_of_sides * area
        # print(f"connected areas {plant_type} -> fence price bulk: {area} * {number_of_sides} = {area * number_of_sides}")

    total_fence_price += fence_price_plant
    total_fence_price_bulk += fence_price_plant_bulk

print("Part 1:", total_fence_price, "\t\tTime:", round(time.time() - t0, 4))
print("Part 1:", total_fence_price_bulk, "\t\tTime:", round(time.time() - t0, 4))
