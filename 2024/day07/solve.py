from functional import seq
import time
from tqdm.auto import tqdm
from ast import literal_eval
import itertools

data = open("input_old").readlines()
# data = open("input").readlines()
t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
results = seq(data).map(lambda x: x.strip().split(":")[0]).map(int).to_list()
number_lists = (
    seq(data).map(lambda x: x.strip().split(":")[1].strip().split(" ")).to_list()
)
number_lists = [list(map(int, nl)) for nl in number_lists]

# ----------------- part 1 --------------
operators1 = ["+", "*"]
valid_result_sum = 0
for result, number_list in tqdm(zip(results, number_lists)):
    # print(result, number_list)
    # the evaluations order is left to right
    operator_combinations = list(
        itertools.product(operators1, repeat=len(number_list) - 1)
    )
    # print(result, number_list, operator_combinations)
    for oc in operator_combinations:
        # expression is evaluated from left to right
        expression = number_list[0]
        for n, op in zip(number_list[1:], oc):
            expression = expression + n if op == "+" else expression * n

        if expression == result:
            # print(expression, "=", result)
            valid_result_sum += result
            break


print("Part 1:", valid_result_sum, "\t\tTime:", round(time.time() - t0, 4))

# ----------------- part 2 --------------
operators1 = ["+", "*", "|"]
valid_result_sum = 0
for result, number_list in tqdm(zip(results, number_lists)):
    # print(result, number_list)
    # the evaluations order is left to right
    operator_combinations = list(
        itertools.product(operators1, repeat=len(number_list) - 1)
    )
    # print(result, number_list, operator_combinations)
    for oc in operator_combinations:
        # expression is evaluated from left to right
        expression = number_list[0]
        for n, op in zip(number_list[1:], oc):
            if op == "*":
                expression = expression * n
            elif op == "+":
                expression = expression + n
            elif op == "|":
                expression = int(f"{expression}{n}")

        if expression == result:
            valid_result_sum += result
            break

print("Part 2:", valid_result_sum, "\t\tTime:", round(time.time() - t0, 4))
