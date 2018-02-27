from EightPuzzle import *
# from IterativeDeepeningSearch import *
from Node import *
from Simple import *
import random


# Global to count nodes expanded.
# DOESNT WORK FOR IDS B/C DIFFERENT CLASS BUT WORKS IN JUPYTER NOTEBOOK
nodesExpanded = 0


# Recursive Best-First Search implementation of the A* algorithm given in class
# Recursive Best First Search (Figure 3.26, Russell and Norvig)
# Recursive Iterative Deepening form of A*, where depth is replaced by f(n)
def aStarSearch(startState, actionsF, takeActionF, goalTestF, hF):
    global nodesExpanded
    nodesExpanded = 0
    h = hF(startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    try:
        result = aStarSearchHelper(startNode, actionsF, takeActionF, goalTestF, hF, float('inf'))
    except RuntimeError as re:
        result = ("failure", float('inf'))
    return result


def aStarSearchHelper(parentNode, actionsF, takeActionF, goalTestF, hF, fmax):
    global nodesExpanded
    if goalTestF(parentNode.state):
        return ([parentNode.state], parentNode.g)
    # print(parentNode)
    # Construct list of children nodes with f, g, and h values
    actions = actionsF(parentNode.state)
    if not actions:
        return ("failure", float('inf'))
    children = []
    for action in actions:
        (childState, stepCost) = takeActionF(parentNode.state, action)
        h = hF(childState)
        g = parentNode.g + stepCost
        f = max(h+g, parentNode.f)
        childNode = Node(state=childState, f=f, g=g, h=h)
        children.append(childNode)
        nodesExpanded += 1
    while True:
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
        if bestChild.f > fmax:
            return ("failure",bestChild.f)

        # next lowest f value
        altf = children[1].f if len(children) > 1 else float('inf')

        # expand best child, reassign its f value to be returned value
        result, bestChild.f = aStarSearchHelper(bestChild, actionsF, takeActionF, goalTestF, hF, min(fmax,altf))
        if result is not "failure":
            result.insert(0, parentNode.state)
            return (result, bestChild.f)


# nNodes = number of nodes expanded during a search
# depth = depth of solution for a search
# returns the
# A well designed heuristic would have a value of b∗ close to 1, allowing fairly large problems to be solved at reasonable computational cost.
def ebf(nNodes, depth, precision=0.01):
    # if nNodes < 1:
    #     raise ValueError('nNodes cant be less than 1 in ebf. Input: ' + str(nNodes))
    # if depth < 0:
    #     raise ValueError('depth cant be less than 0 in ebf. Input: ' + str(depth))

    # if ebfGuess(1, depth) == nNodes:
    #     return 1
    if depth == 0 or nNodes == 1:
        return 1
    # Find range.  Try 10 first and go up by 10s
    low = 1
    high = 10
    while nNodes > ebfGuess(high, depth):
        low = high
        high += 10
    if ebfGuess(high, depth) == nNodes:
        return high

    # print('range is', low, '-', high)
    # Binary search for answer between range
    while True:
        guess = (high + low) / 2
        result = ebfGuess(guess, depth)
        if result-precision <= nNodes <= result+precision:
            return guess
        # print('trying a b value of', guess, 'with range', low, '-', high)
        if result > nNodes:
            high = guess
        else:
            low = guess


def ebfGuess(b, depth):
    result = 0
    for power in range(depth+1):
        result += b**power
    return result


def randomStartState(goalState, actionsF, takeActionF, nSteps):
    state = goalState
    for i in range(nSteps):
        state = takeActionF(state, random.choice(actionsF(state)))[0]
    return state


def runExperiment(goalState1, goalState2, goalState3, hList):
    startState = [1,2,3,4,0,5,6,7,8]

    algs = ['IDS']
    for num in range(len(hList)):
        algs.append('A*h' + str(num+1))

    depths1, nodes1, ebfs1 = experiment(startState, goalState1, hList)
    depths2, nodes2, ebfs2 = experiment(startState, goalState2, hList)
    depths3, nodes3, ebfs3 = experiment(startState, goalState3, hList)

    print('State:    |', goalState1, '|', goalState2, '|', goalState3, '|')
    for row in zip(algs, depths1, nodes1, ebfs1, depths2, nodes2, ebfs2, depths3, nodes3, ebfs3):
        print(row)
    return


# Helper function for runExperiment. Called once per example and returns lists of data
def experiment(startState, goalState, hList):
    global nodesExpanded
    depths = []
    nodes = []
    ebfs = []

    result = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 12)
    depths.append(len(result)-1)
    nodes.append(nodesExpanded)
    est = ebf(nodes[-1], depths[-1]) if nodes[-1] > 0 else 0
    ebfs.append(est)

    for hfxn in hList:
        result = aStarSearch(startState, actionsF_8p, takeActionF_8p,
                             lambda s: goalTestF_8p(s, goalState),
                             lambda s: hfxn(s, goalState))
        depths.append(len(result[0])-1)
        nodes.append(nodesExpanded)
        est = ebf(nodes[-1], depths[-1]) if nodes[-1] > 0 else 0
        ebfs.append(est)

    return depths, nodes, ebfs



if __name__ == '__main__':
    # goalState1 = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    # goalState2 = [1, 2, 3, 4, 5, 8, 6, 0, 7]
    # goalState3 = [1, 0, 3, 4, 5, 8, 2, 6, 7]
    # startState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    # runExperiment(goalState1, goalState2, goalState3, [h1_8p, h2_8p, h3_8p])


    # ass = aStarSearch('a', actionsF_simple, takeActionF_simple,
    #             lambda s: goalTestF_simple(s, 'q'),
    #             lambda s: h_simple(s, 'q'))
    # print(ass)

    hardStart = [8,7,6,5,0,4,3,2,1]
    goalState = [1,2,3,4,0,5,6,7,8]
    pth = aStarSearch(hardStart, actionsF_8p, takeActionF_8p,
                lambda s: goalTestF_8p(s, goalState),
                lambda s: h3_8p(s, goalState))
    printPath_8p(hardStart, goalState, pth[0])
    print(pth[1])

########################################################################################################################
    # ebf testing
    # print(ebf(1000, 7))
    # print(ebf(10, 3)) #1.661376953125
    # print('1.661376953125\n')
    #
    # print(ebf(1, 0))
    # print('1.0\n')
    #
    # print(ebf(2, 1))
    # print('1.0078125\n')
    # # print(ebfGuess_short(1, 1))
    #
    # print(ebf(2, 1, 0.000001))
    # print('1.0000009536743164\n')
    #
    # print(ebf(200000, 5))
    # print('11.275596931956898\n')
    #
    # print(ebf(200000, 50))
    # print('1.2348192492705223\n')
########################################################################################################################


########################################################################################################################
    # Lambda problem - figure out later
    # successors = {'a': ['b', 'c'],
    #               'b': ['d', 'e'],
    #               'c': ['f'],
    #               'd': ['g', 'h'],
    #               'f': ['i', 'j']}
    #
    #
    # def actionsF(s):
    #     try:
    #         ## step cost of each action is 1
    #         return [(succ, 1) for succ in successors[s]]
    #     except KeyError:
    #         return []
    #
    #
    # def takeActionF(s, a):
    #     return a
    #
    #
    # def goalTestF(s):
    #     return s == goal
    #
    #
    # def h1(s):
    #     return 0
    #
    # start = 'a'
    # goal = 'z'
    #
    # result = aStarSearch(start, actionsF, takeActionF,
    #                      lambda s: goalTestF(s, 'z'),
    #                      lambda s: h1(s, 'z'))
    # # result = iterativeDeepeningSearch(start, goal, actionsF, takeActionF, 10)
    # print(result)
    # print('Path from a to h is', result[0], 'for a cost of', result[1])
########################################################################################################################



########################################################################################################################
    # ids = iterativeDeepeningSearch('a', 'z', actionsF_simple, takeActionF_simple, 10)
    # print(ids)
    #
    # star = aStarSearch('a',actionsF_simple, takeActionF_simple,
    #         lambda s: goalTestF_simple(s, 'z'),
    #         lambda s: h_simple(s, 'z'))
    # print(star)
########################################################################################################################





########################################################################################################################
    # actions = actionsF_simple('a')
    # print(actions)
    # print(takeActionF_simple('a', actions[0]))
    # sln = iterativeDeepeningSearch('a', 'z', actionsF_simple, takeActionF_simple, 10)
    # print(sln)
########################################################################################################################

########################################################################################################################
    # goalState = [1,2,3,4,0,5,6,7,8]
    # startState = [1,2,3,4,7,5,6,0,8]
    # newState = takeActionF_8p(startState, ('left',1))[0]
    # sln = iterativeDeepeningSearch(newState, goalState, actionsF_8p, takeActionF_8p, 5)
    # printPath_8p(newState, goalState, sln)
########################################################################################################################

########################################################################################################################
    # goalState = [1,2,3,4,0,5,6,7,8]
    # nSteps = random.randint(0,50)
    # startState = randomStartState(goalState, actionsF_8p, takeActionF_8p, nSteps)
    # # hardStart = [8,7,6,5,0,4,3,2,1]
    # sln = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 25)
    # printPath_8p(startState, goalState, sln)
    #
    # print('Number Shuffle: ', nSteps)
    # print('Solution length: ', len(sln))
    # print('My h fxn: ', h3_8p(startState, goalState))
    #
    # if(h3_8p(startState, goalState) > len(sln)):
    #     print('PROBLEM WITH MY H FXN!!!!')
    #     print('Mine: ', h3_8p(startState, goalState), " -- len(sln): ", len(sln))
########################################################################################################################
