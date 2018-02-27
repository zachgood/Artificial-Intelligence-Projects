debug = False

# Performs an iterative deepening negamax search.  Returns best move for current state and value assosicated
def negamaxIDS(game, maxDepth, utilityFunction = None):
    global debug
    bestValue = -float('infinity')
    bestMove = None
    # bestMove = game.getMoves()[0]
    for depth in range(1, maxDepth+1):
        value, move = negamax(game, depth, utilityFunction)
        # Should I check for failure??????????????????????????
        # Why would negamax return infinity???????????????????
        if value in {None, float('Inf')}: # removed-> , -float('Inf')
            if debug: print('***Depth {} found {} for move {}'.format(depth, value, move))
            continue
        if value == game.getWinningValue(): # Found winning move, so return it
            if debug: print('Found winning value at depth {} with move {}'.format(depth, move))
            return value, move
        if value > bestValue: # Found a new best move
            bestValue = value
            bestMove = move
        if debug:
            print('Depth {} has value {} for move {}'.format(depth, value, move))
            print('AND BestValue {} for BestMove {}'.format(bestValue, bestMove))
    return bestValue, bestMove


# Returns the best move for the current state of the game and the value associated
def negamax(game, depthLeft, utilityFunction = None):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        if debug: print('Negamax Base Case will return ------------------- ', game.getUtility())
        return game.getUtility(utilityFunction), None  # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        # Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1, utilityFunction)
        if debug: print('\tDepth {}, Value {}, Move {}, Player {}'.format(depthLeft, value, move, game.nextPiece))
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    return bestValue, bestMove