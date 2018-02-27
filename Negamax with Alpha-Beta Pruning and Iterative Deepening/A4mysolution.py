from Negamax import *
from NegamaxAB import *
from TicTacToe import *
from PlayGame import *
from EBF import *
from ConnectFour import *
from PlayC4 import *


if __name__ == '__main__':
    # print('negamaxIDSab:')
    # ngmxIDSab_game = TTT()
    # playGame(ngmxIDSab_game, opponent, 10, negamaxIDSab)
    # ngmxIDSab_moves = len(ngmxIDSab_game.locations('X'))
    # ngmxIDSab_nodes = ngmxIDSab_game.getNumberMovesExplored()
    # ngmxIDSab_depth = ngmxIDSab_moves + len(ngmxIDSab_game.locations('O'))
    # ngmxIDSab_ebf = round(ebf(ngmxIDSab_nodes, ngmxIDSab_depth), 2)
    # ngmxIDSab_report = 'negamaxIDSab made {} moves. {} moves explored for ebf({}, {}) of {}'.format(ngmxIDSab_moves,
    #                                                                                                 ngmxIDSab_nodes,
    #                                                                                                 ngmxIDSab_nodes,
    #                                                                                                 ngmxIDSab_depth,
    #                                                                                                 ngmxIDSab_ebf)
    # print(ngmxIDSab_report)
    # negamaxIDSab made 3 moves. 1940 moves explored for ebf(1940, 5) of 4.31


    # Play games
    playGamesC4(dummyC4opp, 4)
    # playGames(dummyTTTopp, 10)
    # game = TTT()
    # playGame(game, UI, 10, negamaxIDSab)
    # playGame(game, UI, 10, negamaxIDS)


    ###############################################
    # Game instance negamaxIDS testing
    # playGame(game, opponent, 10)
    # print('Player {} and Next Up {}'.format(game.player, game.playerLookAHead))
    # print('Utility {}'.format(game.getUtility()))
    # print(negamaxIDS(game, 9))

    ###############################################
    # Play keyboard input
    # letMePlay(game)
    ###############################################

    ###############################################
    # Dummy player vs negamaxIDS
    # playGame(game, opponent, 10)
    ###############################################

    ###############################################
    # Example of draw/cats game
    # print(game)
    # print(game.getUtility())
    # game.makeMove(1)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(0)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(4)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(7)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(3)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(2)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(6)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(5)
    # print(game)
    # print(game.getUtility())
    # game.makeMove(8)
    # print(game)
    # print(game.getUtility())
    ###############################################