from functional import seq
import re
import time

data = open("input").readlines()

t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
def get_mul_output(mul: str) -> int:
    l, r = mul.lstrip("mul(").rstrip(")").split(",")
    return int(l) * int(r)


# ----------------- part 1 --------------
regex = "mul\(\d{1,3},\d{1,3}\)"
matches = re.findall(regex, " ".join(data))

sol = sum(seq(matches).map(get_mul_output))
print("Part 1:", sol, "\t\tTime:", round(time.time() - t0, 4))


# ----------------- part 2 --------------
regex = "mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)"
matches = re.findall(regex, " ".join(data))

sol2 = 0
enabled = True  # by default enabled is True
for m in matches:
    if m == "do()":
        enabled = True
    elif m == "don't()":
        enabled = False
    elif enabled:
        sol2 += get_mul_output(m)

print("Part 2:", sol2, "\t\tTime:", round(time.time() - t0, 4))
