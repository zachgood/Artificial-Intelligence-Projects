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
    succs = []
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            newr = row + r
            newc = col + c
            if 0 <= newr <= 9 and 0 <= newc <= 9:  # cool, huh?
                succs.append( (newr, newc) )
    return succs


def breadthFirstSearch(startState, goalState, successorsf):
	return search(startState, goalState, successorsf, True)
	
	
def depthFirstSearch(startState, goalState, successorsf):
	return search(startState, goalState, successorsf, False)


def search(startState, goalState, successorsf, breadthFirst):
	expanded = {} #visited nodes map to their parent
	unexpanded = [(startState, None)] #touched nodes
	if startState == goalState:
		return [startState]

	while len(unexpanded) != 0:
		eval = unexpanded.pop()
		state = eval[0]
		parent = eval[1]
		children = successorsf(state)
		#Add to expanded dict
		if state not in expanded.keys():
			expanded[state] = parent
		#For efficiency, remove from children any states that are already in expanded or unExpanded.
		visited = [n[0] for n in unexpanded]
		visited += expanded.keys()
		children = [x for x in children if x not in visited]
		
		#Check if goal has been found
		if goalState in children:
			path = [state, goalState]
			
			while parent:
				path.insert(0, parent)
				parent = expanded[parent]
				
			return path
			
		#Sort and reverse children so we all get same solutions
		children.sort()
		children.reverse()
		
		children_mod = [(x,state) for x in children]
		if breadthFirst:
			unexpanded = children_mod + unexpanded
		else:
			unexpanded += children_mod

	return [None]


if __name__ == '__main__':
    print('Breadth-first')
    print('path from a to a is', breadthFirstSearch('a', 'a', successorsf))
    print('NEW path from a to a is', search('a', 'a', successorsf, True))
    print('path from a to m is', breadthFirstSearch('a', 'm', successorsf))
    print('NEW path from a to m is', search('a', 'm', successorsf, True))
    print('path from a to z is', breadthFirstSearch('a', 'z', successorsf))
    print('NEW path from a to z is', search('a', 'z', successorsf, True))
    print('path from a to x is', breadthFirstSearch('a', 'x', successorsf))
    print('NEW path from a to x is', search('a', 'x', successorsf, True))
    print('path from x to a is', breadthFirstSearch('x', 'a', successorsf))
    print('NEW path from x to a is', search('x', 'a', successorsf, True))
    print('path from w to y is', breadthFirstSearch('w', 'y', successorsf))
    print('NEW path from w to y is', search('w', 'y', successorsf, True))
    
    print('Depth-first')
    print('path from a to a is', depthFirstSearch('a', 'a', successorsf))
    print('NEW path from a to a is', search('a', 'a', successorsf, False))
    print('path from a to m is', depthFirstSearch('a', 'm', successorsf))
    print('NEW path from a to m is', search('a', 'm', successorsf, False))
    print('path from a to z is', depthFirstSearch('a', 'z', successorsf))
    print('NEW path from a to z is', search('a', 'z', successorsf, False))
    print('path from h to a is', depthFirstSearch('h', 'a', successorsf)) #none
    print('NEW path from h to a is', search('h', 'a', successorsf, False))
    print('path from c to a is', depthFirstSearch('c', 'a', successorsf))
    print('NEW path from c to a is', search('c', 'a', successorsf, False))
    print('path from c to z is', depthFirstSearch('c', 'z', successorsf))
    print('NEW path from c to z is', search('c', 'z', successorsf, False))
    