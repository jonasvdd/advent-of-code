import numpy as np

with open("input/day02.txt", 'r') as f:
    data = f.readlines()
    l, w, h = np.transpose([np.asarray(line.split('x'), dtype=int) for line in data])

    # part 1
    areas = [l*w, w*h, h*l]
    print("total area: ", np.sum(np.min(areas, axis=0)) + np.sum(2*areas))

    # part 2
    sides = np.sort([l, w, h], axis=0)
    print("length: ", np.sum(l*w*h) + np.sum(2*sides[:2, :]))
