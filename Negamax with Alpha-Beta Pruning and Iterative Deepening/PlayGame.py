from Negamax import *
from NegamaxAB import *
from TicTacToe import *
from EBF import *
from UserInput import *
from ConnectFour import *
from PlayC4 import *

# A dumby opponent
def dummyTTTopp(board):
    return board.index(' ')

# Keyboard input opponent
# def UI(board, valid):
#     moveUI = int(input('Your Move...\n'))
#     while moveUI not in valid:
#         print('\nNOT A VALID MOVE DIP SHIT! >:D\n')
#         print('Pick from one of the following ---> ', valid)
#         moveUI = int(input(''))
#     return moveUI


def playGame(game,opponent,depthLimit, algorithm = negamaxIDS):
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
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)
            print(game)
            game.changePlayer()



def playGames(opponent, depthLimit):
    ngmx_moves = ngmx_nodes = ngmx_depth = ngmx_ebf = None
    ngmxIDS_moves = ngmxIDS_nodes = ngmxIDS_depth = ngmxIDS_ebf = None
    ngmxIDSab_moves = ngmxIDSab_nodes = ngmxIDSab_depth = ngmxIDSab_ebf = None

    # negamax game
    print('negamax:')
    ngmx_game = TTT()
    playGame(ngmx_game, opponent, depthLimit, negamax)
    ngmx_moves = len(ngmx_game.locations('X'))
    ngmx_nodes = ngmx_game.getNumberMovesExplored()
    ngmx_depth = ngmx_moves + len(ngmx_game.locations('O'))
    ngmx_ebf = round(ebf(ngmx_nodes, ngmx_depth), 2)
    ngmx_report = 'negamax made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmx_moves,
                                                                                          ngmx_nodes,
                                                                                          ngmx_nodes,
                                                                                          ngmx_depth,
                                                                                          ngmx_ebf)

    # negamaxIDS game
    print('\nnegamaxIDS:')
    ngmxIDS_game = TTT()
    playGame(ngmxIDS_game, opponent, depthLimit, negamaxIDS)
    ngmxIDS_moves = len(ngmxIDS_game.locations('X'))
    ngmxIDS_nodes = ngmxIDS_game.getNumberMovesExplored()
    ngmxIDS_depth = ngmxIDS_moves + len(ngmxIDS_game.locations('O'))
    ngmxIDS_ebf = round(ebf(ngmxIDS_nodes, ngmxIDS_depth), 2)
    ngmxIDS_report = 'negamaxIDS made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmxIDS_moves,
                                                                                          ngmxIDS_nodes,
                                                                                          ngmxIDS_nodes,
                                                                                          ngmxIDS_depth,
                                                                                          ngmxIDS_ebf)

    print('\nnegamaxIDSab:')
    ngmxIDSab_game = TTT()
    playGame(ngmxIDSab_game, opponent, depthLimit, negamaxIDSab)
    ngmxIDSab_moves = len(ngmxIDSab_game.locations('X'))
    ngmxIDSab_nodes = ngmxIDSab_game.getNumberMovesExplored()
    ngmxIDSab_depth = ngmxIDSab_moves + len(ngmxIDSab_game.locations('O'))
    ngmxIDSab_ebf = round(ebf(ngmxIDSab_nodes, ngmxIDSab_depth), 2)
    ngmxIDSab_report = 'negamaxIDSab made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmxIDSab_moves,
                                                                                                ngmxIDSab_nodes,
                                                                                                ngmxIDSab_nodes,
                                                                                                ngmxIDSab_depth,
                                                                                                ngmxIDSab_ebf)

    print(ngmx_report)
    print(ngmxIDS_report)
    print(ngmxIDSab_report)


