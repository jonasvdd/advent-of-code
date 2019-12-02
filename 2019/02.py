# done processing an opcode -> move to next one by stepping forward 4 positions
import copy

def loop_opcode(orig_data: list):
    data = copy.deepcopy(orig_data)
    opcode = {1: 'sum', 2: 'mult', 99:'halt'}
    for idx in range(0, len(data), 4):
        operation = opcode[data[idx]]
        if operation == 'sum':
            data[data[idx+3]] = data[data[idx+1]] + data[data[idx +2]]
        elif operation == 'mult':
            data[data[idx+3]] = data[data[idx+1]] * data[data[idx +2]]
        elif operation == 'halt':
            return data
    
if __name__ == '__main__':
    # part one
    with open('data/02.txt', 'r') as f:
        data = list(map(int, f.readlines()[0].split(',')))
    data[1] = 12
    data[2] = 2
    
    print(loop_opcode(data)[0])

    # part two
    for noun in range(0, 100):
        for verb in range(0, 100):
            data[1] = noun
            data[2] = verb
            if loop_opcode(data)[0] == 19690720:
                print('noun:', noun, '\tverb:', verb)
