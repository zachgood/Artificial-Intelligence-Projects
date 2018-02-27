from C4Players import *
import C4Fast
import C4Helpers
import Count2WinHeuristic
import Negamax
import NegamaxAB
import OriginalHeuristic
import SimpleHeuristic
import sys
import time
import random
import copy

# THIS MAKES A TIE GAME!!!
# playC4(c4game, lambda game: NegamaxAB.negamaxab(game, 4, Count2WinHeuristic.utility1),
#        lambda game: NegamaxAB.negamaxab(game, 4, Count2WinHeuristic.utility2))

# player1 and player2 should be methods that are passed the game and return a move, score
def playC4(game, player1, player2, track = True):
    path = [game.boardTuple()]
    player1Moves = []
    player1Scores = []
    player1Times = []
    player2Moves = []
    player2Scores = []
    player2Times = []

    if track: print(game)

    while not game.isOver():
        # Player 1 moves
        p1StartTime = time.time()
        p1s, p1m = player1(game)
        player1Times.append(time.time() - p1StartTime)
        if track:
            print('Player 1 moved {} to {} for score {}'.format(game.player, p1m, p1s))
        game.makeMove(p1m)
        if track:
            print(game)
            game.switchPlayer()
        path.append(game.boardTuple())
        player1Moves.append(p1m)
        player1Scores.append(p1s)

        if game.isOver(): break

        # Player 2 moves
        p2StartTime = time.time()
        p2s, p2m = player2(game)
        player2Times.append(time.time() - p2StartTime)
        if track:
            print('Player 2 moved {} to {} for score {}'.format(game.player, p2m, p2s))
        game.makeMove(p2m)
        if track:
            print(game)
            game.switchPlayer()
        path.append(game.boardTuple())
        player2Moves.append(p2m)
        player2Scores.append(p2s)

    won, winner = game.isWon()
    if track:
        if not won: print('Cats game...')
        else: print('Player {} won'.format(winner))
        print('Player 1 moves:', player1Moves)
        print('Player 1 scores:', player1Scores)
        print('Player 1 average move time: {0:.2f}'.format(sum(player1Times)/len(player1Times)))
        print('Player 2 moves:', player2Moves)
        print('Player 2 scores:', player2Scores)
        print('Player 2 average move time: {0:.2f}'.format(sum(player2Times)/len(player2Times)))
        print('Moves explored during this game:', game.movesExplored)
        print('Game history:', game.history)

    return path, player1Moves, player1Scores, player2Moves, player2Scores


# Makes a playoff of all players in playerList
def tournamentC4(playerList, playerNames = None, track = True):
    if playerNames is None:
        playerNames = ['Player ' + str(i + 1) for i in range(len(playerList))]

    firstMoveLossDict = {name: [] for name in playerNames}
    for p1 in range(len(playerList)):
        for p2 in range(len(playerList)):
            if p1 == p2: continue
            if track: print('\n----- Player X: {} vs Player O: {} -----'.format(playerNames[p1], playerNames[p2]))
            tournyGame = C4Fast.C4()
            playC4(tournyGame, playerList[p1], playerList[p2], track)
            if tournyGame.isWon()[1] == 'O':
                firstMoveLossDict[playerNames[p1]].append(playerNames[p2])

    if track:
        for name in playerNames:
            print('{} lost as X Against: {}'.format(name,firstMoveLossDict.get(name)))

    return firstMoveLossDict


if __name__ == '__main__':
    c4game = C4Fast.C4()

    nmwcD4 = lambda game: NegamaxAB.negamaxab(game, 4, C4Helpers.nextMoveWinCount)
    nmwcD6 = lambda game: NegamaxAB.negamaxab(game, 6, C4Helpers.nextMoveWinCount)
    nmwcD8 = lambda game: NegamaxAB.negamaxab(game, 8, C4Helpers.nextMoveWinCount)
    nmwcD10 = lambda game: NegamaxAB.negamaxab(game, 10, C4Helpers.nextMoveWinCount)
    c2w1D2 = lambda game: NegamaxAB.negamaxab(game, 2, Count2WinHeuristic.utility1)
    c2w1D4 = lambda game: NegamaxAB.negamaxab(game, 4, Count2WinHeuristic.utility1)
    c2w1D6 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    c2w2D2 = lambda game: NegamaxAB.negamaxab(game, 2, Count2WinHeuristic.utility2)
    c2w2D4 = lambda game: NegamaxAB.negamaxab(game, 4, Count2WinHeuristic.utility2)
    c2w2D6 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility2)
    c2w3D2 = lambda game: NegamaxAB.negamaxab(game, 2, Count2WinHeuristic.utility3)
    c2w3D4 = lambda game: NegamaxAB.negamaxab(game, 4, Count2WinHeuristic.utility3)
    c2w3D6 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility3)
    playerList = [nmwcD4, nmwcD6, nmwcD8, nmwcD10,
                  c2w1D2, c2w1D4, c2w1D6,
                  c2w2D2, c2w2D4, c2w2D6,
                  c2w3D2, c2w3D4, c2w3D6]
    nameList = ['nmwcD4', 'nmwcD6', 'nmwcD8', 'nmwcD10',
                'c2w1D2', 'c2w1D4', 'c2w1D6',
                'c2w2D2', 'c2w2D4', 'c2w2D6',
                'c2w3D2', 'c2w3D4', 'c2w3D6']
    tournamentC4(playerList, nameList)



    utilityList = [None, C4Helpers.nextMoveWinCount, SimpleHeuristic.utility, OriginalHeuristic.utility,
                   Count2WinHeuristic.utility1, Count2WinHeuristic.utility2, Count2WinHeuristic.utility3]
    utilityNames = ['None', 'Next Move Win Count', 'Simple', 'Original', 'C2W 1', 'C2W 2', 'C2W 3']

    player1 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[0])
    player2 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[1])
    player3 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[2])
    player4 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[3])
    player5 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[4])
    player6 = lambda game: NegamaxAB.negamaxab(game, 4, utilityList[5])
    # tournamentC4([player1, player2, player3, player4, player5, player6], utilityNames)

    # UI VS UI
    # player1 = lambda game: UI(game, SimpleHeuristic.utility)
    # player2 = lambda game: UI(game, SimpleHeuristic.utility)
    # playC4(c4game,
    #        lambda game: UI(game, SimpleHeuristic.utility),
    #        lambda game: UI(game, SimpleHeuristic.utility))

    # NEGAMAXAB VS UI
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, utilityList[4])
    # player2 = lambda game: UI(game) # [3,4,4,3,1,0,4,1,1,2,2]
    # playC4(c4game, player2, player1)


    # NEGAMAXAB VS LIST
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6)
    # # moveList = [3, 2, 3, 3, 4, 0, 5, 6, 3, 0, 1, 6, 4, 6]
    # moveList = [3, 2, 0, 2, 1, 2, 4, 5]
    # player2 = lambda game: listInput(game, moveList, Count2WinHeuristic.utility1)
    # playC4(c4game, player1, player2)

    # NEGAMAXAB VS NEGAMAXAB
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, OriginalHeuristic.utility)
    # player2 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    # playC4(c4game, player2, player1)

    # NEGAMAXAB vs Random
# here
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, OriginalHeuristic.utility)
    # player2 = lambda game: randomMove(game, None)
    # for i in range(10):
    #     print('\nstarting game', i)
    #     newC4 = C4Fast.C4()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.nextPiece is 'X':
    #         lossCounter += 1
    #         print('Game was won by random!')
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    # print('NegamaxAB_Depth6_OrigHeuristic vs random move')
    # print('\twon {} out of 10 games in {} seconds'.format(10-lossCounter, time.time()-startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))
    #
    # print('\nSTARTING NEXT MOVE COUNT HEURISTIC 4 RANDOM\n')
    #
    # # NEGAMAXAB vs Random
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, OriginalHeuristic.utility)
    # player2 = lambda game: randomMove(game, C4Helpers.nextMoveWinCount)
    # for i in range(10):
    #     print('\nstarting game', i)
    #     newC4 = C4Fast.C4()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.nextPiece is 'X':
    #         lossCounter += 1
    #         print('Game was won by random!')
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    # print('NegamaxAB_Depth6_OrigHeuristic vs random move w/ nextMoveWinCounter')
    # print('\twon {} out of 10 games in {} seconds'.format(10 - lossCounter, time.time() - startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))
    #
    # print('\nSTARTING COUNT 2 WIN HEURISTIC\n')
    #
    # # NEGAMAXAB vs Random
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    # player2 = lambda game: randomMove(game, None)
    # for i in range(10):
    #     print('\nstarting game', i)
    #     newC4 = C4Fast.C4()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.nextPiece is 'X':
    #         lossCounter += 1
    #         print('Game was won by random!')
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    # print('NegamaxAB_Depth6_Count2WinHeuristic.utility1 vs random move')
    # print('\twon {} out of 10 games in {} seconds'.format(10 - lossCounter, time.time() - startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))
    #
    # print('\nSTARTING NEXT MOVE WIN HEURISTIC 4 RANDOM\n')
    #
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    # player2 = lambda game: randomMove(game, C4Helpers.nextMoveWinCount)
    # for i in range(10):
    #     print('\nstarting game', i)
    #     newC4 = C4Fast.C4()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.nextPiece is 'X':
    #         lossCounter += 1
    #         print('Game was won by random!')
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    # print('NegamaxAB_Depth6_Count2WinHeuristic.utility1 vs random move w/ nextMoveWinCounter')
    # print('\twon {} out of 10 games in {} seconds'.format(10 - lossCounter, time.time() - startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))

    #################################################################################################



    # # NEGAMAXAB vs Random
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, OriginalHeuristic.utility)
    # player2 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    # for i in range(20):
    #     print('\nRandom start state', i)
    #     newC4 = C4Fast.C4()
    #     newC4.makeRandomMoves(i)
    #     boardSave = copy.deepcopy(newC4.board)
    #     gameStartTime = time.time()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.isWon()[1] is not 'X':
    #         lossCounter += 1
    #         print('Game was won by player 2, O!')
    #         print(boardSave)
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    #     print('\tGame time', time.time() -  gameStartTime)
    #     print('\tGame moves', newC4.movesExplored)
    # print('NegamaxAB_Depth6_OrigHeuristic vs NegamaxAB_Depth6_Count2WinHeuristic.utility1')
    # print('\twon {} out of 10 games in {} seconds'.format(10 - lossCounter, time.time() - startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))
    #
    # print('\nSTARTING NEXT --------------------------\n')
    #
    # lossCounter = 0
    # startTime = time.time()
    # movesExploredCounter = 0
    # player1 = lambda game: NegamaxAB.negamaxab(game, 6, Count2WinHeuristic.utility1)
    # player2 = lambda game: NegamaxAB.negamaxab(game, 6, OriginalHeuristic.utility)
    # for i in range(20):
    #     print('\nRandom start state', i)
    #     newC4 = C4Fast.C4()
    #     newC4.makeRandomMoves(i)
    #     boardSave = copy.deepcopy(newC4.board)
    #     gameStartTime = time.time()
    #     path, player1Moves, player1Scores, player2Moves, player2Scores = playC4(newC4, player1, player2, track=False)
    #     if newC4.isWon()[1] is not 'X':
    #         lossCounter += 1
    #         print('Game was won by player 2, O!')
    #         print(boardSave)
    #         print('Player 1 moves:', player1Moves)
    #         print('Player 1 scores:', player1Scores)
    #         print()
    #         print('Player 2 moves:', player2Moves)
    #         print('Player 2 scores:', player2Scores)
    #         print()
    #         print('Moves explored during this game:', newC4.movesExplored)
    #         print('Game history:', newC4.history)
    #         print(newC4)
    #     movesExploredCounter += newC4.movesExplored
    #     print('\tGame time', time.time() - gameStartTime)
    #     print('\tGame moves', newC4.movesExplored)
    # print('NegamaxAB_Depth6_Count2WinHeuristic.utility1 vs NegamaxAB_Depth6_OrigHeuristic')
    # print('\twon {} out of 10 games in {} seconds'.format(10 - lossCounter, time.time() - startTime))
    # print('\texplored {} moves'.format(movesExploredCounter))




# Player X won
# Player 1 moves: [3, 3, 3, 3, 1, 3, 1, 5, 5, 1, 4, 0, 0, 6, 0, 2, 4, 2, 2]
# Player 1 scores: [-1, 2, 3, 9, 13, 16, 14, 12, 14, 15, 14, 13, 11, 12, 12, 14, 16, 1000, 1000]
# Player 1 average move time: 1.88
# Player 2 moves: [1, 3, 5, 1, 5, 1, 5, 5, 0, 0, 6, 0, 6, 6, 2, 4, 2, 2]
# Player 2 scores: [-12, -8, -4, -4, -7, -2, -2, -10, -7, -12, -15, -22, -16, -31, -500, -500, -1000, -1000]
# Player 2 average move time: 3.57
# Moves explored during this game: 915562