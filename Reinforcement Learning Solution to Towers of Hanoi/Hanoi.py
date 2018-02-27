import copy

def printState(state):
    # Get longest length
    ll = 0
    for prong in state:
        ll = max(ll, len(prong))
    # Add longestLength - length amount of ' ' before each list
    grab = []
    for prong in state:
        numAdd = ll - len(prong)
        grab.append([' ']*numAdd + prong)
    for i in range(ll):
        row = []
        for prong in grab:
            row.append(str(prong[i]))
        print(' '.join(row))
    print('------')


# returns list of moves that are valid from state
def validMoves(state):
    moves = []
    top = []
    for s in state:
        top.append(s[0] if s != [] else float('inf')) # Mark empty pegs as inf
    top = [(en[0]+1, en[1]) for en in enumerate(top)]
    for f in top:
        if f[1] == float('inf'): continue # Cant move from an empty peg
        for t in top:
            if f == t: continue # Cant move to same peg youre from
            if t[1] > f[1]: moves.append([f[0], t[0]])
    return moves


# returns new (copy of) state after move has been applied.
def makeMove(state, move):
    if move not in validMoves(state):
        raise ValueError(str(move) + ' not a valid move for state: ' + str(state))
    stateC = copy.deepcopy(state) # Copy state for manipulation
    piece = stateC[move[0]-1].pop(0) # Remove piece from prong
    stateC[move[1]-1].insert(0,piece) # Put piece on new prong
    return stateC


# returns tuple of state and move.
def stateMoveTuple(state, move):
    stateTup = tuple(tuple(x) for x in state)
    return (stateTup, tuple(move))


# Returns true if Hanoi is complete on the final peg
def winner(state):
    for peg in state[:-1]:
        if peg != []:
            return False
    orderCheck = 1
    for ring in state[-1]:
        if ring != orderCheck:
            return False
        orderCheck += 1
    return True


if __name__ == '__main__':
    winSeq2 = [3, 4, 4, 3, 1, 0, 4, 1, 1, 2, 2]  # Grant's win
    print(listOpp([], winSeq2))
    print(listOpp([], winSeq2))
    print(listOpp([], winSeq2))
    print(listOpp([], winSeq2))



    # Try 4 prongs
    # prong4 = [[1, 2, 3, 4], [], [], []]
    # prong4Win = [[], [], [], [1, 2, 3, 4]]
    # move = [1,4]
    # print(stateMoveTuple(prong4, move))
    # newstate = makeMove(prong4, move)
    # print(newstate)
    # printState(newstate)
    # print(winner(prong4Win))
    # print(validMoves(newstate))


    # Check functions work for 4, 5, 6 disks
    # disk4 = [[1, 2, 3, 4], [], []]
    # disk5 = [[1, 2, 3, 4, 5], [], []]
    # disk6 = [[1, 2, 3, 4, 5, 6], [], []]
    # disk6win = [[], [], [1, 2, 3, 4, 5, 6]]
    # move = [1, 3]
    # print(stateMoveTuple(disk6, move))
    # newstate = makeMove(disk6, move)
    # print(newstate)
    # printState(newstate)
    # print(winner(disk6win))
    # print(validMoves(newstate))

    # These are used for examples below
    # state1 = [[], [1, 2, 3], []]
    # state2 = [[1], [3], [2]]
    # state3 = [[1, 2, 3], [], []]
    # stateWin = [[], [], [1,2,3]]


    # Check winner
    # print(winner(state1))
    # print(winner(state1))
    # print(winner(state1))
    # print(winner(stateWin))


    # stateMoveTuple examples
    # print(stateMoveTuple(state1, [2,1]))
    # state = [[1, 2, 3], [], []]
    # printState(state)
    # move = [1, 2]
    # print(stateMoveTuple(state, move))
    # newstate = makeMove(state, move)
    # print(newstate)
    # printState(newstate)

    # Just some examples
    # s1 = makeMove(state1, validMoves(state1)[0])
    # s2 = makeMove(s1, validMoves(s1)[-1])
    # printState(state1)
    # printState(s1)
    # printState(s2)
    # print(state1 == s2 or state1 == s1)


    # And more examles to check working
    # state3_1 = makeMove(state3, [1,2])
    # state3_2 = makeMove(state3_1, [1,3])
    # state3_3 = makeMove(state3_2, [2,3])
    # printState(state3)
    # printState(state3_1)
    # printState(state3_2)
    # printState(state3_3)
