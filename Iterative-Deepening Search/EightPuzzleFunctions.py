import copy

#Formats 8-puzzle for printing
def printState_8p(state):
    state[state.index(0)] = " "
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])
    state[state.index(" ")] = 0

#Returns index of blank as tuple
def findBlank_8p(state):
    col, row = 0, 0

    #find column
    while col < 3:
        if(0 in state[col::3]): break
        col += 1

    #col = 3 if 0 wasnt in state
    if col == 3:
        raise ValueError('Blank not found in 8-Puzzle!')

    #find row
    for i in state[col::3]:
        if i == 0: break
        row += 1

    return (row, col)

def actionsF_8p(state):
    actions = []
    index = findBlank_8p(state)

    if index[1] > 0:
        actions.append('left')
    if index[1] < 2:
        actions.append('right')
    if index[0] > 0:
        actions.append('up')
    if index[0] < 2:
        actions.append('down')

    return actions

def takeActionF_8p(state, action):
    if action not in actionsF_8p(state):
        raise ValueError(action, 'not valid with blank at index:', findBlank_8p(state))

    here = state.index(0) #Index of blank
    there = state.index(0) #Index of spot to move blank

    if(action == 'left'):
        there -= 1
    if(action == 'right'):
        there += 1
    if(action == 'up'):
        there -= 3
    if(action == 'down'):
        there += 3

    stateC = copy.copy(state)
    stateC[here], stateC[there] = stateC[there], stateC[here]
    return stateC

def printPath_8p(startState, goalState, path):
    print('--Start State--')
    printState_8p(startState)
    print('--End State--')
    printState_8p(goalState)
    print(len(path), ' states for success: ')

    stateNum = 1
    for state in path:
        print('-', stateNum, '-')
        printState_8p(state)
        print()
        stateNum += 1


if __name__ == '__main__':
    startState = [3, 1, 4, 2, 5, 6, 7, 8, 0]
    steps = [startState]
    printState_8p(startState)
    print(findBlank_8p(startState))
    steps.append(takeActionF_8p(steps[-1], 'up'))
    print(steps)
    steps.append(takeActionF_8p(steps[-1], 'left'))
    steps.append(takeActionF_8p(steps[-1], 'left'))
    steps.append(takeActionF_8p(steps[-1], 'up'))
    steps.append(takeActionF_8p(steps[-1], 'right'))
    steps.append(takeActionF_8p(steps[-1], 'down'))
    printPath_8p(steps[0], steps[-1], steps)


    # print(actionsF_8p(startState))
    # steps.append(copy.copy(takeActionF_8p(startState, 'up')))
    # print('up')
    # printState_8p(startState)
    # steps.append(copy.copy(takeActionF_8p(startState, 'left')))
    # print('left')
    # printState_8p(startState)
    # steps.append(copy.copy(takeActionF_8p(startState, 'left')))
    # print('left')
    # printState_8p(startState)
    # steps.append(copy.copy(takeActionF_8p(startState, 'up')))
    # print('up')
    # printState_8p(startState)
    # steps.append(copy.copy(takeActionF_8p(startState, 'right')))
    # print('right')
    # printState_8p(startState)
    # steps.append(copy.copy(takeActionF_8p(startState, 'down')))
    # print('down')
    # printState_8p(startState)
    # goalState = copy.copy(steps[len(steps)-1])
    # firstState = copy.copy(steps[0])
    # printPath_8p(firstState, goalState, steps)

