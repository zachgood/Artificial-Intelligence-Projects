import Negamax
import NegamaxAB
from TicTacToe import *
import sys

# A dumby opponent
def dummyTTTopp(game):
    return game.board.index(' ')

# Keyboard input opponent
def TTT_UI(game):
    validMoves = game.getMoves()
    val = input('Your Move...(or exit with (q)uit)\n')
    if 'q' in val:
        print('Exiting...')
        sys.exit(0)
    try:
        moveUI = int(val)
    except ValueError:
        print('\nThats not an integer!\n')
        return TTT_UI(game)
    if moveUI not in validMoves:
        print('\nNOT A VALID MOVE!\n')
        print('Pick from one of the following ---> ', validMoves)
        return TTT_UI(game)
    return moveUI


def playTTT(game,opponent,depthLimit, algorithm = Negamax.negamax):
    print(game)
    while not game.isOver():
        score,move = algorithm(game,depthLimit)
        if move == None :
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver(): # This section is playing for other player, opponent
            game.changePlayer()
            opponentMove = opponent(game)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)
            print(game)
            game.changePlayer()


def playTTT_1vComp(game,depthLimit,opponent = TTT_UI, algorithm = NegamaxAB.negamaxIDSab):
    comp = 'X'
    print('Move positions:')
    print('{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(0,1,2,3,4,5,6,7,8))
    resp = str.lower(input('Would you like to go first? (Y(es) or N(o))\n'))
    userFirst = False
    if 'n' in resp:
        userFirst = True
        game.makeMove(4)
        comp = 'X'
    print(game)
    print('COMPUTER IS', comp)
    while not game.isOver():
        game.changePlayer()
        opponentMove = opponent(game)
        game.makeMove(opponentMove)
        print('Player', game.player, 'to', opponentMove)
        print(game)
        game.changePlayer()
        # Computer's turn
        if game.isOver():
            break
        score, move = algorithm(game, depthLimit)
        if move == None:
            print('move is None so picking first spot')
            move = game.getMoves()[0]
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score', score)
        print(game)
    if game.getUtility() == 0: print('Cats game... Its a draw!')
    elif len(game.locations('X')) > len(game.locations('O')):
        if userFirst: print('Computer won!')
        else: print('You won!')
    else:
        if not userFirst: print('Computer won!')
        else: print('You won!')
    print('Nodes explored during this game: ', game.getNumberMovesExplored())

# if __name__ == '__main__':
#     playTTT_1vComp(game=TTT(), depthLimit=10, opponent=TTT_UI, algorithm=NegamaxAB.negamaxIDSab)