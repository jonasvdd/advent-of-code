with open("input/day03.txt", 'r') as f:
    data = f.readline() + 'x'

    def calcnewpos(c, x, y):
        if c == '^':
            x += 1
        elif c == '>':
            y += 1
        elif c == '<':
            y -= 1
        elif c == 'v':
            x -= 1
        return x, y

    # part 1
    x, y = 0, 0
    knowledge = {}
    # making data 1 longer to ensure that we also added a 1 in the last calcnewpos 
    for i, c in enumerate(data + "x", 0):
        key = "{}x{}".format(x, y)
        knowledge[key] = 1
        x, y = calcnewpos(c, x, y)
    print("1. houses visited: ", len(knowledge))

    # part 2
    x1, y1, x2, y2 = 0, 0, 0, 0
    knowledge = {}
    # making data 1 longer to ensure that we also added a 1 in the last calcnewpos 
    for i, c in enumerate(data + 'x', 0):  
        if i % 2 == 0:
            key = "{}x{}".format(x2, y2)
            x1, y1 = calcnewpos(c, x1, y1)
        else:
            key = "{}x{}".format(x1, y1)
            x2, y2 = calcnewpos(c, x2, y2)
        knowledge[key] = 1
    print("2. houses visited: ", len(knowledge))
