from Negamax import *
from NegamaxAB import *
from TicTacToe import *
from EBF import *
from UserInput import *
from ConnectFour import *

import random

# A random move C4 opponent
def randomC4opp(game, d = 10):
    moves = game.getMoves()
    return random.choice(moves)

# A dummy algorithm
def dummyAlg(game, d):
    moves = game.getMoves()
    return 0, moves[0]

# A dumby opponent
def dummyC4opp(game):
    moves = game.getMoves()
    return moves[0]

# def C4UI(game):
#     validMoves = game.getMoves()
#     moveUI = int(input('Your Move...\n'))
#     while moveUI not in validMoves:
#         print('\nNOT A VALID MOVE! >:D\n')
#         print('Pick from one of the following ---> ', validMoves)
#         moveUI = int(input(''))
#     return moveUI


def playGameC4(game,opponent,depthLimit, algorithm = negamaxIDS):
    print(game)
    while not game.isOver():
        score,move = algorithm(game,depthLimit)
        if move == None :
            move = dummyC4opp(game)
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
    _,winner = game.isWon()
    print('Player {} won!'.format(winner))
    print('Nodes explored during this game: ', game.getNumberMovesExplored())


def playC4_1vComp(game,depthLimit,opponent = UI, algorithm = dummyAlg):
    comp = 'X'
    print('Connect Four (C4)© v-2.0 \t\t\t\t\t Depth :', depthLimit, '\n')
    resp = str.lower(input('Would you like to go first? (Y(es) or N(o))\n'))
    if 'n' in resp:
        game.makeMove(3)
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
    won, winner = game.isWon()
    if not won:
        print('Cats game... Its a draw!')
    elif winner is comp:
        print('HAHAHAHA I WIN!!!!!!')
    else:
        print('No way you won!?!?!?')
    print('Player {} won!'.format(winner))
    print('Nodes explored during this game: ', game.getNumberMovesExplored())


def playC4_1v1(game):
    print(game)
    while not game.isOver():
        move = UI(game)
        game.makeMove(move)
        print('Player', game.player, 'to', move)
        print(game)
        game.changePlayer()
    won, winner = game.isWon()
    print('Player {} won!'.format(winner))


def playC4_CvC(game, depthLimit, alg1 = dummyAlg, alg2 = negamaxIDSab):
    print(game)
    while not game.isOver():
        score, move = alg1(game, depthLimit)
        if move == None:
            move = alg1(game)
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score', score)
        print(game)
        if not game.isOver():  # This section is playing for other player, opponent
            game.changePlayer()
            opponentScore, opponentMove = alg2(game, depthLimit)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove, 'for score', opponentScore)
            print(game)
            game.changePlayer()
    _, winner = game.isWon()
    print('Player {} won!'.format(winner))
    print('Nodes explored during this game: ', game.getNumberMovesExplored())


def playTTT_1vComp(game,depthLimit,opponent = UI, algorithm = dummyAlg):
    comp = 'X'
    resp = str.lower(input('Would you like to go first? (Y(es) or N(o))\n'))
    if 'n' in resp:
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
    elif len(game.locations('X')) > len(game.locations('O')): print('HAHAHAHA I WIN!!!!!!')
    else: print('No way you won!?!?!?')
    print('Game Utility: ', game.getUtility())
    print('Nodes explored during this game: ', game.getNumberMovesExplored())


def playGamesC4(opponent, depthLimit):
    ngmx_moves = ngmx_nodes = ngmx_depth = ngmx_ebf = None
    ngmxIDS_moves = ngmxIDS_nodes = ngmxIDS_depth = ngmxIDS_ebf = None
    ngmxIDSab_moves = ngmxIDSab_nodes = ngmxIDSab_depth = ngmxIDSab_ebf = None

    # negamax game
    print('negamax:')
    ngmx_game = C4()
    playGameC4(ngmx_game, opponent, depthLimit, negamax)
    ngmx_moves = ngmx_game.locations('X')
    ngmx_nodes = ngmx_game.getNumberMovesExplored()
    ngmx_depth = ngmx_moves + ngmx_game.locations('O')
    ngmx_ebf = round(ebf(ngmx_nodes, ngmx_depth), 2)
    ngmx_report = 'negamax made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmx_moves,
                                                                                          ngmx_nodes,
                                                                                          ngmx_nodes,
                                                                                          ngmx_depth,
                                                                                          ngmx_ebf)

    # negamaxIDS game
    print('\nnegamaxIDS:')
    ngmxIDS_game = C4()
    playGameC4(ngmxIDS_game, opponent, depthLimit, negamaxIDS)
    ngmxIDS_moves = ngmxIDS_game.locations('X')
    ngmxIDS_nodes = ngmxIDS_game.getNumberMovesExplored()
    ngmxIDS_depth = ngmxIDS_moves + ngmxIDS_game.locations('O')
    ngmxIDS_ebf = round(ebf(ngmxIDS_nodes, ngmxIDS_depth), 2)
    ngmxIDS_report = 'negamaxIDS made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmxIDS_moves,
                                                                                          ngmxIDS_nodes,
                                                                                          ngmxIDS_nodes,
                                                                                          ngmxIDS_depth,
                                                                                          ngmxIDS_ebf)

    print('\nnegamaxIDSab:')
    ngmxIDSab_game = C4()
    playGameC4(ngmxIDSab_game, opponent, depthLimit, negamaxIDSab)
    ngmxIDSab_moves = ngmxIDSab_game.locations('X')
    ngmxIDSab_nodes = ngmxIDSab_game.getNumberMovesExplored()
    ngmxIDSab_depth = ngmxIDSab_moves + ngmxIDSab_game.locations('O')
    ngmxIDSab_ebf = round(ebf(ngmxIDSab_nodes, ngmxIDSab_depth), 2)
    ngmxIDSab_report = 'negamaxIDSab made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmxIDSab_moves,
                                                                                                ngmxIDSab_nodes,
                                                                                                ngmxIDSab_nodes,
                                                                                                ngmxIDSab_depth,
                                                                                                ngmxIDSab_ebf)

    print(ngmx_report)
    print(ngmxIDS_report)
    print(ngmxIDSab_report)


if __name__ == '__main__':
    TTTgame = TTT()
    C4game = C4()
    # playGameC4(C4game, UI, 6, negamaxIDSab)  # User vs negamaxIDSab connect four
    #############################################################################
    # playGameC4(C4game, UI, 4, negamaxIDSab) # User vs negamaxIDSab connect four
    playC4_1vComp(C4game, 6, opponent=UI, algorithm=negamaxIDSab)
    winSeq = [3,1,3,2,5,0,3,6,0,1,1,0,2,5,6,6,5,6,4] # Kolton's win
    winSeq2 = [3,4,4,3,1,0,4,1,1,2,2] # Grant's win
    #############################################################################
    # playC4_CvC(C4game, 4, negamaxIDS)
    # playTTT_1vComp(TTTgame, 10, opponent = C4UI, algorithm = dummyAlg)
    # playC4_1vComp(C4game, 4, opponent = UI, algorithm = negamaxIDSab)

    # game = C4()
    # # playC4_1vComp(game, 10, opponent = C4UI, algorithm = negamaxIDSab)
    # playC4_1v1(game)