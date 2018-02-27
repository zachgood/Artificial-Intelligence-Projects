import numpy as np
import random
from copy import deepcopy
import time
from C4Helpers import *
import OriginalHeuristic
import Count2WinHeuristic
import SimpleHeuristic

# Almost full board example
# _ 0 _ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _
# 0 X | O | O |   | X | X | X |
# |---+---+---+---+---+---+---|
# 1 O | X | X | O | O | X | O |
# |---+---+---+---+---+---+---|
# 2 X | X | X | O | X | O | O |
# |---+---+---+---+---+---+---|
# 3 O | O | X | O | X | X | X |
# |---+---+---+---+---+---+---|
# 4 O | O | O | X | O | O | X |
# |---+---+---+---+---+---+---|
# 5 O | O | X | X | O | X | X |

#
# # Sets player and player look ahead.  Idk if this is the best way to do this...
# def setPlayer(self, piece):
#     self.player = piece
#     self.playerLookAHead = self.player

class C4(object):

    def __init__(self, load = False, randomStart = False):
        self.nextPiece = 'X'  # Next piece to be dropped
        if load: # Used to start a game at a different state.  Just change to true to use
            self.board = [['O', 'X', 'O', 'O', 'O', 'X', ' '],
                          ['X', 'O', 'X', 'X', 'X', 'O', ' '],
                          ['O', 'X', 'O', 'O', 'O', 'X', ' '],
                          ['X', 'O', 'X', 'X', 'X', 'O', 'X'],
                          ['O', 'X', 'O', 'O', 'O', 'X', 'O'],
                          ['X', 'O', 'X', 'X', 'X', 'O', 'X']]
            self.nextPiece = 'O'

            # [['O', 'X', 'O', 'O', 'O', 'X', 'O'],
            #  ['X', 'O', 'X', 'X', 'X', 'O', 'X'],
            #  ['O', 'X', 'O', 'O', 'O', 'X', 'O'],
            #  ['X', 'O', 'X', 'X', 'X', 'O', 'X'],
            #  ['O', 'X', 'O', 'O', 'O', 'X', 'O'],
            #  ['X', 'O', 'X', 'X', 'X', 'O', 'X']] # THIS IS A TIE GAME

            # [[' ', ' ', 'O', ' ', ' ', ' ', ' '],
            #  [' ', ' ', 'X', ' ', ' ', ' ', ' '],
            #  [' ', ' ', 'O', 'O', ' ', ' ', ' '],
            #  [' ', ' ', 'O', 'X', ' ', ' ', ' '],
            #  [' ', 'X', 'X', 'O', ' ', ' ', ' '],
            #  ['O', 'X', 'X', 'X', 'O', ' ', ' ']]

            # [[' ', ' ', ' ', 'X', ' ', ' ', ' '],
            #  [' ', 'O', ' ', 'O', ' ', ' ', ' '],
            #  [' ', 'X', ' ', 'O', ' ', ' ', ' '],
            #  ['X', 'O', 'O', 'O', ' ', ' ', ' '],
            #  ['X', 'X', 'O', 'X', ' ', ' ', ' '],
            #  ['X', 'X', 'O', 'X', 'O', 'X', 'O']]
        else:
            self.board = [[' ' for x in range(7)] for y in range(6)] # Make a 7x6 board
        self.history = [] # List of moves in order
        self.startTime = time.time()
        self.player = 'X' # Player that is currently up.  Kinda like 'whos perspective' b/c it doesnt change every move
        self.movesExplored = 0  # Counter for number of moves explored
        self.winningValue = 1000  # Winning number for game utility
        if randomStart:
            nMoves = random.choice(range(1,43))
            print('Starting game with {} random moves'.format(nMoves))
            self.makeRandomMoves(nMoves)

    # To string
    def __str__(self):
        top = '_ 0 _ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _\n'
        # bottom = '\n----------------------------- Next Piece: {} - Utility: {}'.format(self.nextPiece, self.getUtility())
        bottom = '\n-----------------------------'
        boardData = []
        rowIndex = 0
        for row in self.board:
            boardData.append(str(rowIndex) + ' {} | {} | {} | {} | {} | {} | {} |'.format(*row))
            rowIndex += 1
        printBoard = top + '\n|---+---+---+---+---+---+---|\n'.join(boardData) + bottom
        return printBoard

    # Tuple of board row by row, starting at 0
    def boardTuple(self):
        return tuple(tuple(x) for x in self.board)

    # Number of seconds that game has been being played for
    def getPlayTime(self):
        return time.time() - self.startTime

    # Switches player
    def switchPlayer(self):
        self.player = 'O' if self.player is 'X' else 'X'

    # Switches next piece placed
    def switchNextPiece(self):
        self.nextPiece = 'O' if self.nextPiece is 'X' else 'X'

    # Places piece at row, col on board
    def placePiece(self, piece, row, col):
        self.board[row][col] = piece

    # Returns piece at row, col on board
    def getSpot(self, row, col):
        return self.board[row][col]

    # returns rows of board in a list (basically just the board)
    def getRows(self):
        return self.board

    # returns columns of board in a list
    def getColumns(self):
        return [list(x) for x in zip(*self.board)]

    # returns diagonal down lists of board
    def getDiagDown(self):
        return [[self.board[2][0], self.board[3][1], self.board[4][2], self.board[5][3]],
                [self.board[1][0], self.board[2][1], self.board[3][2], self.board[4][3], self.board[5][4]],
                [self.board[0][0], self.board[1][1], self.board[2][2], self.board[3][3], self.board[4][4], self.board[5][5]],
                [self.board[0][1], self.board[1][2], self.board[2][3], self.board[3][4], self.board[4][5], self.board[5][6]],
                [self.board[0][2], self.board[1][3], self.board[2][4], self.board[3][5], self.board[4][6]],
                [self.board[0][3], self.board[1][4], self.board[2][5], self.board[3][6]]]

    # returns diagonal up lists of board
    def getDiagUp(self):
        return [[self.board[3][0], self.board[2][1], self.board[1][2], self.board[0][3]],
                [self.board[4][0], self.board[3][1], self.board[2][2], self.board[1][3], self.board[0][4]],
                [self.board[5][0], self.board[4][1], self.board[3][2], self.board[2][3], self.board[1][4], self.board[0][5]],
                [self.board[5][1], self.board[4][2], self.board[3][3], self.board[2][4], self.board[1][5], self.board[0][6]],
                [self.board[5][2], self.board[4][3], self.board[3][4], self.board[2][5], self.board[1][6]],
                [self.board[5][3], self.board[4][4], self.board[3][5], self.board[2][6]]]

    # returns list of lists for each row, column, and diagonal
    def getGroups(self):
        all = []
        all.extend(self.getRows())
        all.extend(self.getColumns())
        all.extend(self.getDiagDown())
        all.extend(self.getDiagUp())
        return all

    # Returns number of open spots
    def countOpen(self):
        openCounter = 0
        for i in range(6):
            # openCounter += len(C4Helpers.find(self.board[i], ' '))
            openCounter += len(find(self.board[i], ' '))
        return openCounter

    # # Returns columns that are not full
    def getMoves(self):
        return find(self.board[0], ' ')
    # Returns columns that are not full
    # def getMoves(self):
    #     moves = []
    #     index = 0
    #     for spot in self.board[0]:
    #         if spot is ' ':
    #             moves.append(index)
    #         index += 1
    #     return moves

    # Puts the current player's mark at the column index passed.
    # Changes nextPiece because the next move is going to be made by the other player
    def makeMove(self, move):
        if move not in self.getMoves():
            if move is None:
                raise ValueError('None not a valid column to make move!' + self)
            raise ValueError(str(move) + ' not a valid column to make move!' + self)
        # Get row index to put piece
        rowIndex = max(find(self.getColumns()[move], ' ')) # max(C4Helpers.find(self.getColumns()[move], ' '))
        # Place piece in column
        self.board[rowIndex][move] = self.nextPiece
        # Put the move in the history
        self.history.append(move)
        # Switch next piece to place
        self.nextPiece = 'X' if self.nextPiece == 'O' else 'O'
        # Count move
        self.movesExplored += 1

    # Removes mark from index passed and restores nextPiece b/c that move was taken back
    def unmakeMove(self, move):
        if not 0 <= move <= 6:
            raise ValueError(str(move) + ' not a valid column to remove piece from!')

        # Get row index of top piece
        currCol = self.getColumns()[move]
        if 'X' not in currCol and 'O' not in currCol:
            raise ValueError('Cant remove piece from empty column ' + str(move))
        if ' ' not in currCol:
            rowIndex = 0
        else:
            rowIndex = min([i for i, ltr in enumerate(currCol) if ltr != ' '])

        # Remove piece in column
        self.board[rowIndex][move] = ' '
        # Remove that move from history
        self.history.reverse()
        self.history.remove(move)
        self.history.reverse()
        # Switch player look ahead
        self.nextPiece = 'X' if self.nextPiece == 'O' else 'O'

    # Makes nMoves number of random moves that dont end game
    # DOESNT ALWAYS MAKE THAT MANY MOVES.  WILL RETURN IF ALL MOVES ON A TURN END THE GAME
    # Returns False if it didnt make that many moves
    def makeRandomMoves(self, nMoves):
        for i in range(nMoves):
            moves = self.getMoves()
            randomMove = random.choice(moves)
            moves.remove(randomMove)
            self.makeMove(randomMove)
            while self.isOver():
                self.unmakeMove(randomMove)
                if len(moves) < 1: return False
                randomMove = random.choice(moves)
                moves.remove(randomMove)
                self.makeMove(randomMove)
        return True

    def isWon(self): # Previously named isWonMegaFast
        # The following line makes a single string of all rows, columns, and diagonals.
        # spots are not separated by a space but each group is seperated by a space to avoid incorrect 4 in a row
        groupsAsString = ' '.join([''.join(x) for x in self.getGroups()])
        if 'X' * 4 in groupsAsString: return True, 'X'
        elif 'O' * 4 in groupsAsString: return True, 'O'
        else: return False, ' '

    # Returns True if game is over, False otherwise
    def isOver(self):
        if self.isFull(): return True
        return self.isWon()[0]

    # Returns true if board is full
    def isFull(self):
        return not ' ' in self.board[0]

    # Returns information on the state of the board:
    #   1 = a player has won and is next up
    #   -1 = a player has won and not next up
    #   0 = game is a draw, no one wins
    #   None if the game is still being played
    # Returns the 'value' of the game in the perspective of the next piece to go
    # Larger number => better state
    def getUtility(self, utilityFunction = nextMoveWinCount): # USED TO BE SIMPLE HEURISTIC
        won, winner = self.isWon()
        if winner is 'X': return 1000 if self.nextPiece is 'X' else -1000
        elif winner is 'O': return 1000 if self.nextPiece is 'O' else -1000
        elif self.isFull(): return 0
        else:
            utilityValue = utilityFunction(self) if utilityFunction is not None else 0
            return utilityValue if self.nextPiece is 'X' else (utilityValue * -1)


if __name__ == '__main__':
    c4 = C4(True)
    print(c4)
    c4.makeMove(1)
    c4.makeMove(1)
    print(c4)
    print(c4.isOver())



    # TESTING IS WON FUNCTIONS ########################################
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = c4f.isWon()
    # print(time.time() - startTime)  # 3.809983253479004
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = c4f.isWonEvenFaster()
    # print(time.time() - startTime)  # 2.773622989654541
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = c4f.isWonMegaFast()
    # print(time.time() - startTime)  # 2.1786561012268066
    # ###################################################################
