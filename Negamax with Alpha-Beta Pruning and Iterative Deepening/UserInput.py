from Negamax import *
from TicTacToe import *


# Keyboard input opponent
def UI(game):
    validMoves = game.getMoves()
    moveUI = int(input('Your Move...\n'))
    while moveUI not in validMoves:
        print('\nNOT A VALID MOVE! >:D\n')
        print('Pick from one of the following ---> ', validMoves)
        moveUI = int(input(''))
    return moveUI


def letMePlay(game):
    # Play keyboard input
    resp = str.lower(input('Would you like to go first? (Y or N)\n'))
    if 'y' in resp:
        playGameUI_MeFirst(game, UI, 10)
    else:
        playGameUI(game, UI, 10)
    # Game over
    if game.getUtility() == 0:
        print('Cats game... Its a draw!')
    elif len(game.locations('X')) > len(game.locations('O')):
        print('HAHAHAHA I WIN!!!!!!')
    else:
        print('No way you won!?!?!?')
    print('Game Utility: ', game.getUtility())
    print('Nodes explored during this game: ', game.getNumberMovesExplored())


def playGameUI(game,opponent,depthLimit):
    print(game)
    while not game.isOver():
        if game.isEmpty():
            # score = float('inf')
            score = 0
            move = game.board.index(' ')
        else:
            score, move = negamaxIDS(game, depthLimit)
        if move == None :
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver(): # This section is playing for other player, opponent
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)
            print(game)
            game.changePlayer()


def playGameUI_MeFirst(game,opponent,depthLimit):
    print(game)
    while not game.isOver():
        # This section is for UI to make move
        opponentMove = opponent(game.board)
        game.makeMove(opponentMove)
        print('Player', game.player, 'to', opponentMove)
        print(game)
        if not game.isOver(): # This section is AI making decision
            game.changePlayer()
            score, move = negamaxIDS(game, depthLimit)
            if move == None :
                print('move is None. Stopping.')
                break
            game.makeMove(move)
            print('Player', game.player, 'to', move, 'for score' ,score)
            print(game)
            game.changePlayer()



if __name__ == '__main__':
    print('hello...')