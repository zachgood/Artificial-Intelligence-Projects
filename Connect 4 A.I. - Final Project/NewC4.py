import numpy as np
from copy import deepcopy
import time

# Returns true and piece of 4IAR if list has 4 pieces in a row (IAR), false and ' ' otherwise
def has4IAR(group):
    lookFor = ' '
    cons = 0
    for spot in group:
        if spot == lookFor:
            cons += 1
        else:
            lookFor = spot
            cons = 1
        if cons == 4 and lookFor != ' ':
            return True, lookFor
    return False, ' '


def has4IARFaster(group): # a little faster
    groupAsString = ''.join(group)
    if 'X'*4 in groupAsString: return True, 'X'
    elif 'O'*4 in groupAsString: return True, 'O'
    else: return False, ' '


class NC4(object):

    def __init__(self, load = False):
        self.board = np.array([[' ' for x in range(7)] for y in range(6)])  # Make a 7x6 board
        self.player = 'X' # Player that is currently up
        if load: # Used to start a game at a different state.  Just change to true to use
            self.board = np.array([[' ', ' ', 'O', ' ', ' ', ' ', ' '],
                                   [' ', ' ', 'X', ' ', ' ', ' ', ' '],
                                   [' ', ' ', 'O', 'O', ' ', ' ', ' '],
                                   [' ', ' ', 'O', 'X', ' ', ' ', ' '],
                                   [' ', 'X', 'X', 'O', ' ', ' ', ' '],
                                   ['O', 'X', 'X', 'X', 'O', ' ', ' ']])
            self.player = 'X'
        self.playerLookAHead = self.player # Next player to move
        self.movesExplored = 0 # Counter for number of moves explored
        self.winningValue = 1000 # Winning move number when negamax searching -- 4 in a row

    # To string
    def __str__(self):
        top = '_ 0 _ 1 _ 2 _ 3 _ 4 _ 5 _ 6 _\n'
        bottom = '\n-----------------------------'
        boardData = []
        rowIndex = 0
        for row in self.board:
            boardData.append(str(rowIndex) + ' {} | {} | {} | {} | {} | {} | {} |'.format(*row))
            rowIndex += 1
        printBoard = top + '\n|---+---+---+---+---+---+---|\n'.join(boardData) + bottom
        return printBoard

    # returns rows of board in a list (basically just the board)
    def getRows(self):
        return [self.board[x, :] for x in range(6)]

    # returns each row of board as string, all in a list
    def getStringRows(self):
        return [''.join(self.board[x, :]) for x in range(6)]

    # returns columns of board in a list
    def getColumns(self):
        return [self.board[:, x] for x in range(7)]

    # returns each column of board as string, all in a list
    def getStringColumns(self):
        return [''.join(self.board[:, x]) for x in range(7)]

    # returns diagonal down lists of board
    def getDiagDown(self):
        return [self.board.diagonal(x) for x in range(-2, 4)]

    # returns all diagonal downs as strings, all in a list
    def getStringDiagDown(self):
        return [''.join(self.board.diagonal(x)) for x in range(-2, 4)]

    # returns diagonal up lists of board
    def getDiagUp(self):
        return [np.flip(self.board, 1).diagonal(x) for x in range(-2, 4)]

    # returns all diagonal up as strings, all in a list
    def getStringDiagUp(self):
        return [''.join(np.flip(self.board, 1).diagonal(x)) for x in range(-2, 4)]

    # returns list of numpy arrays for each row, column, and diagonal
    def getGroups(self):
        all = []
        all.extend(self.getRows())
        all.extend(self.getColumns())
        all.extend(self.getDiagDown())
        all.extend(self.getDiagUp())
        return all

    # Returns columns that are not full
    def getMoves(self):
        return np.where(self.board[0] == ' ')[0]

    # Puts the current player's mark at the column index passed.
    # Changes playerLookAhead because the next move is going to be made by the other player
    def makeMove(self, move):
        if move not in self.getMoves():
            raise ValueError(str(move) + ' not a valid column to make move!')
        # Get row index to put piece
        rowIndex = np.argmax(np.where(self.board[:, move] == ' ')[0])
        # Place piece in column
        self.board[rowIndex][move] = self.playerLookAHead
        # Switch player
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        # Count move
        self.movesExplored += 1

    # Removes mark from index passed and restores playerLookAHead b/c that move was taken back
    def unmakeMove(self, move):
        if not 0 <= move <= 6:
            raise ValueError(str(move) + ' not a valid column to remove piece from!')

        # Get row index of top piece
        currCol = self.board[:, move]
        if 'X' not in currCol and 'O' not in currCol:
            raise ValueError('Cant remove piece from empty column ' + str(move))
        if ' ' not in self.board[:, move]:
            rowIndex = 0
        else:
            rowIndex = min(np.where(self.board[:, move] != ' ')[0])

        # Remove piece in column
        self.board[rowIndex][move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def isWon(self):
        # Check row win
        for row in self.board:
            boo, winner = has4IAR(row)
            if boo: return True, winner
        # Check column win
        for col in self.getColumns():
            boo, winner = has4IAR(col)
            if boo: return True, winner
        # Check diagonal down win
        for d in self.getDiagDown():
            boo, winner = has4IAR(d)
            if boo: return True, winner
        # Check diagonal up win
        for d in self.getDiagUp():
            boo, winner = has4IAR(d)
            if boo: return True, winner
        return False, ' '

    def isWonFaster(self):
        # Check row win
        for row in self.getStringRows():
            if 'XXXX' in row: return True, 'X'
            if 'OOOO' in row: return True, 'O'
        # Check column win
        for col in self.getStringColumns():
            if 'XXXX' in col: return True, 'X'
            if 'OOOO' in col: return True, 'O'
        # Check diagonal down win
        for dd in self.getStringDiagDown():
            if 'XXXX' in dd: return True, 'X'
            if 'OOOO' in dd: return True, 'O'
        # Check diagonal up win
        for du in self.getStringDiagUp():
            if 'XXXX' in du: return True, 'X'
            if 'OOOO' in du: return True, 'O'
        return False, ' '

    def isWonEvenFaster(self):
        for g in self.getGroups():
            boo, winner = has4IARFaster(g)
            if boo: return boo, winner
        return False, ' '

    def isWonMegaFast(self):
        # The following line makes a single string of all rows, columns, and diagonals.
        # spots are not separated by a space but each group is seperated by a space to avoid incorrect 4 in a row
        groupsAsString = ' '.join([''.join(x) for x in self.getGroups()])
        if 'X' * 4 in groupsAsString: return True, 'X'
        elif 'O' * 4 in groupsAsString: return True, 'O'
        else: return False, ' '



# Returns list of all indices in string/list 's' that are char 'ch'
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

{
# Returns the number of single spots in a row, col, or diag that would make 4 in a row
# def one2win(group, piece):
#     # if there are less than 3 of piece in the group, cant get 4 in a row, so return 0
#     if len(find(group, piece)) < 3:
#         return 0
#     print('starting win counter with group ', group)
#     winCounter = 0
#     emptySpots = find(group, ' ')
#     for spot in emptySpots:
#         group[spot] = piece
#         print('Checking win for group ', group)
#         if piece*4 in ''.join(group): winCounter += 1
#         group[spot] = ' '
#     print('ended with group ', group)
#     return winCounter


# Returns the number of spot pairs in a row, col, or diag that would make 4 in a row
# def two2win(group, piece):
#     # if there are less than 3 of piece in the group, cant get 4 in a row, so return 0
#     if len(find(group, piece)) < 2:
#         return 0
#     print('starting win counter with group ', group)
#     winCounter = 0
#     emptySpots = find(group, ' ')
#     for i in range(len(emptySpots)):
#         group[emptySpots[i]] = piece
#         for j in range(i-1):
#             if spot == spot2: continue
#             group[emptySpots[j]] = piece
#             print('Checking win for group ', group)
#             if piece*4 in ''.join(group): winCounter += 1
#             group[spot2] = ' '
#         group[spot] = ' '
#     print('ended with group ', group)
#     return winCounter
}

# Returns counts for number of single, double, and triple spots in given group that would make 4 in a row for piece type
# count2win([' ', 'X', 'O', 'X', 'X', ' ', ' '], 'O') => 0, 1, 1 is an non-optimal example b/c win is counted twice
def count2win(group, piece):
    print('In count to win with group {} and piece {}'.format(group, piece))
    count1 = count2 = count3 = 0
    emptySpots = find(group, ' ')
    for i in range(len(emptySpots)):
        group[emptySpots[i]] = piece # print('Checking win for group ', group)
        if piece * 4 in ''.join(group):
            count1 += 1
            group[emptySpots[i]] = ' '
            continue # Because we dont want to count the win twice.  Like, once for 4 in a row and once for 5 in a row
        for j in range(i+1, len(emptySpots)):
            group[emptySpots[j]] = piece # print('\tChecking win for group ', group)
            if piece * 4 in ''.join(group):
                count2 += 1
                group[emptySpots[j]] = ' '
                continue # Same thing here
            for k in range(j+1, len(emptySpots)):
                group[emptySpots[k]] = piece # print('\t\tChecking win for group ', group)
                if piece * 4 in ''.join(group):
                    count3 += 1
                group[emptySpots[k]] = ' '
            group[emptySpots[j]] = ' '
        group[emptySpots[i]] = ' '
    return count1, count2, count3


if __name__ == '__main__':
    nc4 = NC4()
    print(nc4)

    # rows = deepcopy(nc4.getRows())
    # rows = nc4.getRows()
    # arow = rows[5]
    #
    # print(two2win(arow, 'X'))
    # print(nc4)

    XfullCount1 = XfullCount2 = XfullCount3 = 0
    OfullCount1 = OfullCount2 = OfullCount3 = 0
    for g in nc4.getGroups():
        print(type(g))
        Xcount1, Xcount2, Xcount3 = count2win(g, 'X')
        XfullCount1 += Xcount1
        XfullCount2 += Xcount2
        XfullCount3 += Xcount3
        Ocount1, Ocount2, Ocount3 = count2win(g, 'O')
        OfullCount1 += Ocount1
        OfullCount2 += Ocount2
        OfullCount3 += Ocount3
    print(XfullCount1, XfullCount2, XfullCount3)
    print(OfullCount1, OfullCount2, OfullCount3)

    #Checking win for group  ['O', 'X', 'O', 'X', 'X', ' ', ' ']
# 	Checking win for group  ['O', 'X', 'O', 'X', 'X', 'O', ' ']
# 		Checking win for group  ['O', 'X', 'O', 'X', 'X', 'O', 'O']
# 	Checking win for group  ['O', 'X', 'O', 'X', 'X', ' ', 'O']
# Checking win for group  [' ', 'X', 'O', 'X', 'X', 'O', ' ']
# 	Checking win for group  [' ', 'X', 'O', 'X', 'X', 'O', 'O']
# Checking win for group  [' ', 'X', 'O', 'X', 'X', ' ', 'O']






    # TESTING IS WON FUNCTIONS ########################################
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.isWon()
    # print(time.time() - startTime) # 16.005241870880127
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.isWonFaster()
    # print(time.time() - startTime) # 15.548794269561768
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.isWonEvenFaster()
    # print(time.time() - startTime)  # 16.031381845474243
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.isWonMegaFast()
    # print(time.time() - startTime) # 14.019618034362793
    # ####################################################################

    # TESTING GET ROWS W/ & W/O DEEPCOPY #################################
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.getRows()
    # print(time.time() - startTime) # 0.028497934341430664
    #
    # startTime = time.time()
    # for i in range(100000):
    #     ddown = nc4.getRowsCopy()
    # print(time.time() - startTime) # 0.5347011089324951
    # ####################################################################


    # indxs = np.where(nc4.board[:, 5] != ' ')[0]
    # print(len(indxs))
    # print(min(indxs))
    # print(np.argmax(np.where(nc4.board[:, 2] == ' ')[0]) + 1)