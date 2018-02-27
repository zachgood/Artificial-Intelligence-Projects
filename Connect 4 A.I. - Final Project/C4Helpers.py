import C4Fast
import random

# Returns true and piece of 4IAR if list has 4 pieces in a row (IAR), false and ' ' otherwise
def has4IARFaster(group): # a little faster
    groupAsString = ''.join(group)
    if 'X'*4 in groupAsString: return True, 'X'
    elif 'O'*4 in groupAsString: return True, 'O'
    else: return False, ' '


# Returns list of all indices in string/list 's' that are char 'ch'
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


# Returns count of moves from getMoves() that result in win.  Mult by -1 if x up next b/c it is for utility
def nextMoveWinCount(C4game):
    winCount = 0
    for move in C4game.getMoves():
        C4game.makeMove(move)
        if C4game.isOver(): winCount += 1
        C4game.unmakeMove(move)
    return winCount if C4game.nextPiece is 'X' else (winCount * -1)


# Returns an unwon C4 game with nMoves random moves
def randomBoard(nMoves = None):
    # COULD ADD IN A MOVE TRACKER TO AVOID HAVING TO RETURN A GAME WITH NO MOVES LEFT...
    randomC4 = C4Fast.C4()
    if nMoves is None: nMoves = random.choice(range(0, 40))
    print('nMoves is ', nMoves)
    for i in range(nMoves):
        moves = randomC4.getMoves()
        randomMove = random.choice(moves)
        moves.remove(randomMove)
        randomC4.makeMove(randomMove)
        while randomC4.isWon()[0]:
            randomC4.unmakeMove(randomMove)
            if len(moves) < 1: return randomC4
            randomMove = random.choice(moves)
            moves.remove(randomMove)
            randomC4.makeMove(randomMove)
    return randomC4


if __name__ == '__main__':
    # c4 = C4Fast.C4(randomStart=True)
    c4 = randomBoard()
    print(c4.playerLookAHead)
    print(c4)
    print(c4.countOpen())


