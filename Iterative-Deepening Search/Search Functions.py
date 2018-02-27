from EightPuzzleFunctions import *
import random

def iterativeDeepeningSearch(startState, goalState, actionsF, takeActionF, maxDepth):
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState, actionsF, takeActionF, depth)
        if result == 'failure':
            return 'failure'
        if result != 'cutoff':
            result.insert(0, startState)
            return result
    return 'cutoff'

def depthLimitedSearch(startState, goalState, actionsF, takeActionF, depthLimit):
    return recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit)

def recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit):
    # print('startState: {}\ndepthLimit: {}\npath: {}\n'.format(startState, depthLimit, path))
    if startState == goalState:
        return []
    elif depthLimit == 0:
        return 'cutoff'
    else:
        cuttoffOccured = False
        for action in actionsF(startState):
            child = takeActionF(startState, action)
            result = recursiveDLS(child, goalState, actionsF, takeActionF, depthLimit-1)
            if result == 'cutoff':
                cuttoffOccured = True
            elif result != 'failure':
                # print(depthLimit, result, child)
                result.insert(0, child)
                return result
        if cuttoffOccured:
            return 'cutoff'
        else:
            return 'failure'

#
# def startRecur(start, end, depthLimit):
#     return recur(start, end, depthLimit, [])
#
# def recur(start, end, depthLimit, path):
#     if start == end:
#         return end
#     elif depthLimit == 0:
#         return 'cutoff'
#     else:
#         cuttoffOccured = False
#         child = start - 1
#         path.append(child)
#         result = recur(child, end, depthLimit-1, path)
#         # path.append(child)
#         if result == 'cutoff':
#             cuttoffOccured = True
#         elif result != 'failure':
#             return path
#         if cuttoffOccured:
#             return 'cutoff'
#         else:
#             return 'failure'

def randomStartState(goalState, actionsF, takeActionF, nSteps):
    state = goalState
    for i in range(nSteps):
        state = takeActionF(state, random.choice(actionsF(state)))
    return state

if __name__ == '__main__':
    goalState = [1,2,3,4,0,5,6,7,8]
    # startState = randomStartState(goalState, actionsF_8p, takeActionF_8p, 10)
    startState = [1, 5, 0, 4, 7, 2, 6, 8, 3]
    path = iterativeDeepeningSearch(startState, goalState, actionsF_8p, takeActionF_8p, 20)
    print(path)
    printPath_8p(startState, goalState, path)

    # check = startRecur(3, 1, 5)
    # print(check)


# def depthLimitedSearch(startState, goalState, actionsF, takeActionF, depthLimit):
#     return recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit, [])
#
# def recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit, path):
#     # print('startState: {}\ndepthLimit: {}\npath: {}\n'.format(startState, depthLimit, path))
#     if startState == goalState:
#         return goalState
#     elif depthLimit == 0:
#         return 'cutoff'
#     else:
#         cuttoffOccured = False
#         path.insert(0, startState)
#         for action in actionsF(startState):
#             child = takeActionF_8p(startState, action)
#             # path.append(child)
#             result = recursiveDLS(child, goalState, actionsF, takeActionF, depthLimit-1, path)
#             if result == 'cutoff':
#                 cuttoffOccured = True
#             elif result != 'failure':
#                 path.append(goalState)
#                 return path
#         if cuttoffOccured:
#             return 'cutoff'
#         else:
#             return 'failure'