import copy

# Formats 8-puzzle for printing
def printState_8p(state):
    state[state.index(0)] = " "
    print(state[0], state[1], state[2])
    print(state[3], state[4], state[5])
    print(state[6], state[7], state[8])
    state[state.index(" ")] = 0


# Returns index of blank as tuple
def findBlank_8p(state):
    return findIndex_8p(state, 0)


# Returns index of specific piece
def findIndex_8p(state, piece):
    col, row = 0, 0

    # find column
    while col < 3:
        if piece in state[col::3]: break
        col += 1

    # col = 3 if piece wasnt in state
    if col == 3:
        raise ValueError(str(piece) + ' not found in 8-Puzzle!')

    # find row
    for i in state[col::3]:
        if i == piece: break
        row += 1

    return (row, col)


def actionsF_8p(state):
    actions = []
    index = findBlank_8p(state)

    if index[1] > 0:
        actions.append(('left',1))
    if index[1] < 2:
        actions.append(('right',1))
    if index[0] > 0:
        actions.append(('up',1))
    if index[0] < 2:
        actions.append(('down',1))

    return actions


def takeActionF_8p(state, action):
    if action not in actionsF_8p(state):
        raise ValueError(str(action) + ' not valid with blank at index: ' + str(findBlank_8p(state)))

    here = state.index(0) #Index of blank
    there = state.index(0) #Index of spot to move blank
    move = action[0]
    cost = action[1]

    if(move == 'left'):
        there -= 1
    if(move == 'right'):
        there += 1
    if(move == 'up'):
        there -= 3
    if(move == 'down'):
        there += 3

    stateC = copy.copy(state)
    stateC[here], stateC[there] = stateC[there], stateC[here]
    return (stateC, cost)


def goalTestF_8p(state, goal):
    return state == goal


def printPath_8p(startState, goalState, path):
    print('--Start State--')
    printState_8p(startState)
    print('--End State--')
    printState_8p(goalState)

    if isinstance(path, str):
        print('Path not found: ', path)
        return

    print(len(path), ' states for success: ')

    stateNum = 1
    for state in path:
        print('-', stateNum, '-')
        printState_8p(state)
        print()
        stateNum += 1


# Heuristic Functions
# h(state,goal) = 0, for all states 'state' and all goal states 'goal'
def h1_8p(state, goal):
    return 0


# Returns the Manhattan distance that the piece is from its goal position
def mDist(state, goal, piece):
    m = 0
    indexS = findIndex_8p(state, piece)
    indexG = findIndex_8p(goal, piece)
    m += abs(indexS[0] - indexG[0])
    m += abs(indexS[1] - indexG[1])
    return m


# h(state,goal) = m, where m is the Manhattan distance that the blank is from its goal position
def h2_8p(state, goal):
    return mDist(state, goal, 0)


# h(state,goal) = a, where a is the summation of the Manhattan distance
# that all pieces are from their goal position excluding the blank
def h3_8p(state, goal):
    a = 0
    for piece in range(1,9):
        a += mDist(state, goal, piece)
    return a


if __name__ == '__main__':
    goalState = [1,2,3,4,0,5,6,7,8]
    steps = [goalState]
    # steps.insert(0, takeActionF_8p(steps[0], ('right', 1))[0])
    # steps.insert(0, takeActionF_8p(steps[0], ('down', 1))[0])
    # steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    # steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('right', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('down', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('up', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('up', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('right', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('down', 1))[0])

    steps.insert(0, takeActionF_8p(steps[0], ('right', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('down', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('up', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('left', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('up', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('right', 1))[0])
    steps.insert(0, takeActionF_8p(steps[0], ('down', 1))[0])

    printState_8p(steps[0])
    printState_8p(goalState)
    print(h3_8p(steps[0], goalState))

