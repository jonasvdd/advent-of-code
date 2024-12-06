from functional import seq
from typing import Dict, Set
import time

# data = open("input_old").readlines()
data = open("input").readlines()

t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
ordering_rules = (
    seq(data).filter(lambda x: "|" in x).map(lambda x: x.strip().split("|"))
)
ordering_rules = [[int(el) for el in row] for row in ordering_rules]

page_numbers = seq(data).filter(lambda x: "," in x).to_list()
page_numbers = seq(page_numbers).map(lambda x: x.strip()).map(lambda x: x.split(","))
page_numbers = [[int(el) for el in row] for row in page_numbers]

# print(ordering_rules)
# print(page_numbers)

must_come_after : Dict[int, Set[int]]= {}
for el in ordering_rules:
    if el[0] not in must_come_after:
        must_come_after[el[0]] = {el[1]}
    else:
        must_come_after[el[0]].add(el[1])
# print(must_come_after)


def check_valid_order(page_order):
    valid_order = True
    for i, pn in enumerate(page_order[1:], 1):
        pages_after = must_come_after.get(pn, set())
        if len(pages_after.intersection(page_order[:i])):
            valid_order = False
            break
    return valid_order


def reorder_invalid_order(page_order: list) -> list:
    new_page_order = page_order.copy()

    i = 1
    while i < len(new_page_order):
        pn = new_page_order[i]
        pages_after = must_come_after.get(pn, set())
        if len(pages_after.intersection(new_page_order[:i])):
            # swap the previous page with the current page
            new_page_order[i - 1], new_page_order[i] = (
                new_page_order[i],
                new_page_order[i -1],
            )
            i = 1  # reset the loop
        else:
            i += 1

    return new_page_order


# ----------------- part 1 --------------
num_valid_orders = 0

for page_order in page_numbers:
    if check_valid_order(page_order):
        # add the middle page
        num_valid_orders += page_order[(len(page_order) - 1) // 2]

print("Part 1:", num_valid_orders, "\t\tTime:", round(time.time() - t0, 4))


# ----------------- part 2 --------------
middle_sum = 0
for page_order in page_numbers:
    valid_order = check_valid_order(page_order)

    if not valid_order:
        # ensure that the data is correctly ordered
        correct_page_order = reorder_invalid_order(page_order)
        # add the middle page
        middle_sum += correct_page_order[(len(page_order) - 1) // 2]


print("Part 2:", middle_sum, "\t\tTime:", round(time.time() - t0, 4))
