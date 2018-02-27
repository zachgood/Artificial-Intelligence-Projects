successors = {'a':  ['b', 'c', 'd'],
              'b':  ['e', 'f', 'g'],
              'c':  ['a', 'h', 'i'],
              'd':  ['j', 'z'],
              'e':  ['k', 'l'],
              'g':  ['m'],
              'k':  ['z']}

import copy

def successorsf(state):
    return copy.copy(successors.get(state, []))
    
def gridSuccessors(state):
    row, col = state
    # succs will be list of tuples () rather than list of lists [] because state must
    # be an immutable type to serve as a key in dictionary of expanded nodes
    succs = [(),()]
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            newr = row + r
            newc = col + c
            if 0 <= newr <= 9 and 0 <= newc <= 9:  # cool, huh?
                succs.append( (newr, newc) )
    return succs

def camelSuccessorsf(camelStartState):
    succs = []
    #Get index of empty space
    startSpaceIndex = camelStartState.index(' ')
    
    #Get info that wont change on the left and right
    hardLeft = camelStartState[0:max(startSpaceIndex - 2, 0)]
    hardRight = camelStartState[min(startSpaceIndex + 3, 9):9]
    mid = camelStartState[max(startSpaceIndex - 2, 0):min(startSpaceIndex + 3, 9)]
    
    spaceIndex = mid.index(' ')
    #Check options on left
    if 'R' in mid[:spaceIndex]:
    	#Option for camel on left of space to move right
    	mid_leftOp = list(mid)
    	switchIndex = -1
    	if mid[spaceIndex-1] == 'R':
            #switch space with index one to the left
    		switchIndex = spaceIndex-1
    	else: #if mid[spaceIndex-2] == 'L':
    		#Switch space with index two to the left
    		switchIndex = spaceIndex-2
    	a, b = mid_leftOp[switchIndex], mid_leftOp[spaceIndex]
    	mid_leftOp[switchIndex], mid_leftOp[spaceIndex] = b, a
    	combine_leftOp = hardLeft + tuple(mid_leftOp) + hardRight
    	succs.append(combine_leftOp)
    
    #Check Options on right
    if 'L' in mid[spaceIndex+1:]:
    	#Option for camel on right of space to move left
    	mid_rightOp = list(mid)
    	switchIndex = -1
    	if mid[spaceIndex+1] == 'L':
    		#switch space with index one to the right
    		switchIndex = spaceIndex+1
    	else: #if mid[spaceIndex+2] == 'R':
    		#Switch space with index two to the right
    		switchIndex = spaceIndex+2
    	a, b = mid_rightOp[switchIndex], mid_rightOp[spaceIndex]
    	mid_rightOp[switchIndex], mid_rightOp[spaceIndex] = b, a
    	combine_rightOp = hardLeft + tuple(mid_rightOp) + hardRight
    	succs.append(combine_rightOp)
    	
    return succs
    
    
    
    # mid_right = copy.copy(mid)
#     spaceIndex = mid.index(' ')
#     if spaceIndex == 0:
#     	if mid[1] == 'L':
#     		mid_right = (
    


if __name__ == '__main__':
#     print(successorsf('c'))
#     print(successorsf('v'))
#     print(gridSuccessors([3,4]))
#     print(gridSuccessors([0,0]))
    #Camel stuff
    camelStartState = ('R', 'R', 'R', 'R', ' ', 'L', 'L', 'L', 'L')
    camelGoalState = ('L', 'L', 'L', 'L', ' ', 'R', 'R', 'R', 'R')
    check = ('R', 'R', 'R', 'L', ' ', 'R', 'L', 'L', 'L')
    print("State: ", check)
    print("Successers: ", camelSuccessorsf(check))
