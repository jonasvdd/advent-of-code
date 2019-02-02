with open("input/day01.txt", 'r') as f:
    # part 1
    data = f.readline()
    floor = data.count('(') - data.count(')')
    print(floor)

    # part 2
    floor = 0
    for i, c in enumerate(data, 1):
        floor += 1 if c == '(' else -1
        if floor == -1:
            print("i: {}, floor: {}".format(i, floor))
            break
