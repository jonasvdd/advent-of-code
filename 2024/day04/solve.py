from functional import seq
import numpy as np
import time

# data = open("input_old").readlines()
data = open("input").readlines()

t0 = time.time()  # data I/O doesn't count in the time


# ----------------- shared --------------
data = seq(data).map(lambda x: x.strip()).map(list).to_pandas().values


def print_data(d: np.ndarray):
    for row in d:
        print("".join(row))


def get_word_mask(data: np.ndarray, word: str, x_shift, y_shift) -> np.ndarray:
    first_letter_mask = data == word[0]
    direction_mask = first_letter_mask

    # now find matches in all directions
    for i, letter in enumerate(word[1:], start=1):
        roll_mask = np.roll(data == letter, (y_shift * i, x_shift * i), axis=(0, 1))
        # mask the areas which were rolled out of the array
        if x_shift == 1:
            roll_mask[:, x_shift * (i - 1)] = False
        elif x_shift == -1:
            roll_mask[:, x_shift * i] = False

        if y_shift == 1:
            roll_mask[y_shift * (i - 1), :] = False
        elif y_shift == -1:
            roll_mask[y_shift * i, :] = False

        direction_mask &= roll_mask
    return direction_mask


# ----------------- part 1 --------------
# start finding matches from the start letter
total_mask = np.zeros(data.shape).astype(bool)
matches = 0
# fmt: off
for x_shift, y_shift in [
    # lr and rl (horizonal)
    (-1, 0), (1, 0),
    # vertical
    (0, 1), (0, -1),
    # diagonal
    (1, 1), (-1, -1), (1, -1), (-1, 1),
]:
    direction_mask = get_word_mask(data, "XMAS", x_shift=x_shift, y_shift=y_shift) 
    matches += np.sum(direction_mask)

    # expand the mask to the whole word
    direction_mask_exp = np.copy(direction_mask)
    for i in range(1, len("XMAS")):
        direction_mask_exp |= np.roll(direction_mask, (-y_shift * i, -x_shift * i), axis=(0, 1))

    data_cp = np.copy(data)
    data_cp[~direction_mask_exp] = "."
    total_mask |= direction_mask_exp
    # print((x_shift, y_shift), "matches:", np.sum(direction_mask))
    # print_data(data_cp)

# print("Total mask")
# data_cp = np.copy(data)
# data_cp[~total_mask] = "."
# print_data(data_cp)

print("Part 1:", matches, "\t\tTime:", round(time.time() - t0, 4))


# ----------------- part 2 --------------
total_mask = np.zeros(data.shape).astype(bool)
matches = 0
for shift1, shift2 in [
    ((-1, 1), (-1, -1)),
    ((1, -1), (-1, -1)),
    ((1, 1), (-1, -1)),
    ((1, 1), (1, -1)),
    ((1, 1), (-1, 1)),
    ((1, -1), (-1, 1)),
]:
    # now find matches in all directions
    x_shift1, y_shift1 = shift1
    direction_mask1 = get_word_mask(data, "MAS", x_shift=x_shift1, y_shift=y_shift1) 

    x_shift2, y_shift2 = shift2
    direction_mask2 = get_word_mask(data, "MAS", x_shift=x_shift2, y_shift=y_shift2)

    # expand the mask to the whole word
    # direction_mask1_exp = np.copy(direction_mask1)
    # for i in range(1, len("MAS")):
    #     direction_mask1_exp |= np.roll(direction_mask1, (-y_shift1 * i, -x_shift1 * i), axis=(0, 1))
    # print('--'*30)
    # print(f'direction_mask1_exp - {x_shift1, y_shift1}')
    # data_cp = np.copy(data)
    # data_cp[~direction_mask1_exp] = "."
    # # print_data(direction_mask1_exp.astype(int).astype(str))
    # print_data(data_cp)

    # direction_mask2_exp = np.copy(direction_mask2)
    # for i in range(1, len("MAS")):
    #     direction_mask2_exp |= np.roll(direction_mask2, (-y_shift2 * i, -x_shift2 * i), axis=(0, 1))
    # print(f'direction_mask2_exp - {x_shift2, y_shift2}')
    # data_cp = np.copy(data)
    # data_cp[~direction_mask2_exp] = "."
    # # print_data(direction_mask2_exp)
    # print_data(data_cp)

    # center the mask around the second letter of the word
    direction_mask1 = np.roll(direction_mask1, (-y_shift1, -x_shift1), axis=(0, 1))
    direction_mask2 = np.roll(direction_mask2, (-y_shift2, -x_shift2), axis=(0, 1))

    matches += np.sum(direction_mask1 & direction_mask2)


print("Part 2:", matches, "\t\tTime:", round(time.time() - t0, 4))
