debug = False

# negamaxIDS but with alpha beta pruning
def negamaxIDSab(game, maxDepth, utilityFunction = None, alpha = -float('Inf'), beta = float('Inf'), skipOdds = False):
    global debug
    bestValue = -float('infinity')
    bestMove = None
    # bestMove = game.getMoves()[0]
    for depth in range(1, maxDepth + 1):
        if skipOdds and depth%2 != 0:
            continue
        value, move = negamaxab(game, depth, utilityFunction)
        if value in {None, float('Inf')}:  # removed-> , -float('Inf')
            if debug: print('***Depth {} found {} for move {}'.format(depth, value, move))
            continue
        if value == game.winningValue:  # Found winning move, so return it
            if debug: print('Found winning value at depth {} with move {}'.format(depth, move))
            return value, move
        if value > bestValue:  # Found a new best move
            bestValue = value
            bestMove = move
        if debug:
            print('Depth {} has value {} for move {}'.format(depth, value, move))
            print('AND BestValue {} for BestMove {}.  Nodes explored: {}.'.format(bestValue, bestMove, game.movesExplored))
    return bestValue, bestMove


# Negamax search but with alpha beta pruning
def negamaxab(game, depthLeft, utilityFunction = None, alpha = -float('Inf'), beta = float('Inf')):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        # print(utilityFunction)
        # print(None)
        # utilityValue = game.getUtility(utilityFunction) if utilityFunction is not None else 0
        # print(utilityValue)
        return game.getUtility(utilityFunction), None
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    # Swap and negate alpha beta
    alpha, beta = -beta, -alpha
    if debug:
        print('{}\n^Game in ngmxAB -> Depth Left: {}, alpha: {}, beta: {}'.format(game, depthLeft, alpha, beta))
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)

        # Use depth-first search to find eventual utility value and back it up.
        value, _ = negamaxab(game, depthLeft - 1, utilityFunction, alpha, beta)

        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue

        # Negate it because it will come back in context of next player
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move

        # Update alpha to maximum of bestScore and current alpha
        alpha = max(bestValue, alpha)

        if debug: print('\tmove {} has value: {}, alpha: {}, beta: {}, bestValue: {}, bestMove: {}'.format(move, value, alpha, beta, bestValue, bestMove))

        # Do early return if bestScore is greater than or equal to beta
        if bestValue >= beta:
            if debug:
                print('*PRUNE FOUND AT DEPTHLEFT {}* move {}. bestValue: {}, beta: {}, bestMove: {}'.format(depthLeft, move, bestValue, beta, bestMove))
            return bestValue, bestMove
    return bestValue, bestMove