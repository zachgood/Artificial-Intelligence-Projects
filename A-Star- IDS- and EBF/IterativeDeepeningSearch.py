def iterativeDeepeningSearch(startState, goalState, actionsF, takeActionF, maxDepth):
    global nodesExpanded
    nodesExpanded = 0
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState, actionsF, takeActionF, depth)
        print('ids - ', nodesExpanded)
        if result == 'failure':
            return 'failure'
        if result != 'cutoff':
            result.insert(0, startState)
            return result
    return 'cutoff'


def depthLimitedSearch(startState, goalState, actionsF, takeActionF, depthLimit):
    return recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit)


def recursiveDLS(startState, goalState, actionsF, takeActionF, depthLimit):
    global nodesExpanded
    # print('startState: {}\ndepthLimit: {}\npath: {}\n'.format(startState, depthLimit, path))
    if startState == goalState:
        return []
    elif depthLimit == 0:
        return 'cutoff'
    else:
        cuttoffOccured = False
        for action in actionsF(startState):
            child,_ = takeActionF(startState, action)
            nodesExpanded += 1
            print('**********')
            result = recursiveDLS(child, goalState, actionsF, takeActionF, depthLimit-1)
            if result == 'cutoff':
                cuttoffOccured = True
            elif result != 'failure':
                # print(depthLimit, result, child)
                result.insert(0, child)
                print(nodesExpanded)
                return result
        if cuttoffOccured:
            return 'cutoff'
        else:
            return 'failure'
