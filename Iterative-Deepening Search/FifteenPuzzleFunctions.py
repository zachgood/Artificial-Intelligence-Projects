import copy

#Formats 15-puzzle for printing
def printState_15p(state):
    state[state.index(0)] = " "
    print(state[0], state[1], state[2], state[3])
    print(state[4], state[5], state[6], state[7])
    print(state[8], state[9], state[10], state[11])
    print(state[12], state[13], state[14], state[15])
    state[state.index(" ")] = 0

#Returns index of blank as tuple
def findBlank_15p(state):
    col, row = 0, 0

    #find column
    while col < 4:
        if(0 in state[col::4]): break
        col += 1

    #col = 3 if 0 wasnt in state
    if col == 4:
        raise ValueError('Blank not found in 15-Puzzle!')

    #find row
    for i in state[col::4]:
        if i == 0: break
        row += 1

    return (row, col)

def actionsF_15p(state):
    actions = []
    index = findBlank_15p(state)

    if index[1] > 0:
        actions.append('left')
    if index[1] < 3:
        actions.append('right')
    if index[0] > 0:
        actions.append('up')
    if index[0] < 3:
        actions.append('down')

    return actions

def takeActionF_15p(state, action):
    if action not in actionsF_15p(state):
        raise ValueError(action, 'not valid with blank at index:', findBlank_15p(state))

    here = state.index(0) #Index of blank
    there = state.index(0) #Index of spot to move blank

    if(action == 'left'):
        there -= 1
    if(action == 'right'):
        there += 1
    if(action == 'up'):
        there -= 4
    if(action == 'down'):
        there += 4

    stateC = copy.copy(state)
    stateC[here], stateC[there] = stateC[there], stateC[here]
    return stateC

def printPath_15p(startState, goalState, path):
    print('--Start State--')
    printState_15p(startState)
    print('--End State--')
    printState_15p(goalState)
    print(len(path), ' states for success: ')

    stateNum = 1
    for state in path:
        print('-', stateNum, '-')
        printState_15p(state)
        print()
        stateNum += 1


if __name__ == '__main__':
    startState = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    steps = [startState]
    printState_15p(startState)
    print(findBlank_15p(startState))
    steps.append(takeActionF_15p(steps[-1], 'up'))
    print(steps)
    steps.append(takeActionF_15p(steps[-1], 'left'))
    steps.append(takeActionF_15p(steps[-1], 'left'))
    steps.append(takeActionF_15p(steps[-1], 'up'))
    steps.append(takeActionF_15p(steps[-1], 'right'))
    steps.append(takeActionF_15p(steps[-1], 'down'))
    printPath_15p(steps[0], steps[-1], steps)