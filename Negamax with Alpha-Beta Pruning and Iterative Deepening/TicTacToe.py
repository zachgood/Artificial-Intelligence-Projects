debug = False

class TTT(object):

    def __init__(self):
        self.board = [' ']*9
        self.player = 'X' # Player that is currently up
        if False: # Used to start a game at a different state.  Just change to true to use
            self.board = ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O']
            self.player = 'X'
        self.playerLookAHead = self.player # Next player to move
        self.movesExplored = 0 # Counter for number of moves explored
        self.winningValue = 1 # Winning move number when negamax searching

    # Returns the locations of X's, O's, or empty spots (c) for board
    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    # Returns empty spot locations of board
    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        # Get locations of X's
        whereX = self.locations('X')
        # Get locations of O's
        whereO = self.locations('O')
        # Lists of locations that would constitute a win
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        # Boolean that checks if X has won
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        # Boolean that checks if O has won
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            # If X has won and is the next player to move, return 1
            # If X has won but is not the next player to move, return -1
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            # If O has won and is the next player to move, return 1
            # If O has won but is not the next player to move, return -1
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            # If there is a draw (Cats game) return 0
            return 0
        else:
            # If the game is still being played, return None
            return None  ########################################################## CHANGED FROM -0.1

    # Returns True if game is over, False otherwise
    def isOver(self):
        return self.getUtility() is not None

    # Puts the current player's mark at the index passed.  DOESNT CHECK TO MAKE SURE THAT MOVE IS VALID...
    # Changes playerLookAhead because the next move is going to be made by the other player
    def makeMove(self, move):
        global debug
        self.board[move] = self.playerLookAHead
        if debug: print('MADE MOVE ', self.playerLookAHead, ' @ SPOT, ', move)
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        if debug: print('CHANGED NEXT UP TO: ', self.playerLookAHead)

    # Changes player.  Also changes playerLookAHead because the new player hasnt made move yet so they are next up
    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player
        global debug
        if debug: print('CHANGED PLAYER TO: ', self.player)

    # Removes mark from index passed and restores playerLookAHead b/c that move was taken back
    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        global debug
        if debug: print('UNMADE MOVE: ', move)

    # Returns the number of moves explored
    def getNumberMovesExplored(self):
        return self.movesExplored

    # Returns the number representing a win when negamax searching
    def getWinningValue(self):
        return self.winningValue

    def isEmpty(self):
        boo = True
        for i in self.board:
            if not i.isspace():
                boo = False
        return boo

    # To string
    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s