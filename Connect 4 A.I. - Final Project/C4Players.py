import sys
import time
import random
import copy


# List of moves in order opponent
def listInput(game, moveList, utilityFunction = None):
    moveFromList = moveList.pop(0)
    # Get score that move produces
    game.makeMove(moveFromList)
    scoreFromList = game.getUtility(utilityFunction)
    game.unmakeMove(moveFromList)
    return scoreFromList, moveFromList


# Keyboard input opponent
def UI(game, utilityFunction = None):
    val = input('Move... (or exit with (q)uit)\n')

    # Check quit
    if 'q' in val:
        print('Exiting...')
        sys.exit(0)

    # Check valid int
    try:
        moveUI = int(val)
    except ValueError:
        print('\nThats not an integer!\n')
        return UI(game)

    # Check valid move
    validMoves = game.getMoves()
    if moveUI not in validMoves:
        print('\nNOT A VALID MOVE! >:D\n')
        print('Pick from one of the following ---> ', validMoves)
        return UI(game)

    # Get score that move produces
    game.makeMove(moveUI)
    scoreUI = game.getUtility(utilityFunction)*-1
    game.unmakeMove(moveUI)
    return scoreUI, moveUI


# Player makes random move from moves that generate highest game utility using utility function
def randomMove(game, utilityFunction = None):
    d = dict.fromkeys(game.getMoves(), 0)
    for move in d.keys():
        game.makeMove(move)
        d[move] = game.getUtility(utilityFunction)*-1
        game.unmakeMove(move)
    listOfBestMoves = [k for k,v in d.items() if v == max(d.values())]
    randomMove = random.choice(listOfBestMoves)
    return d[randomMove], randomMove