debug = False

class C4(object):

    def __init__(self, load = False):
        self.board = [[' ' for x in range(7)] for y in range(6)] # Make a 7x6 board
        self.player = 'X' # Player that is currently up
        if load: # Used to start a game at a different state.  Just change to true to use
            self.board = [[' ', ' ', 'O', ' ', ' ', ' ', ' '],
                                   [' ', ' ', 'X', ' ', ' ', ' ', ' '],
                                   [' ', ' ', 'O', 'O', ' ', ' ', ' '],
                                   [' ', ' ', 'O', 'X', ' ', ' ', ' '],
                                   [' ', 'X', 'X', 'O', ' ', ' ', ' '],
                                   ['O', 'X', 'X', 'X', 'O', ' ', ' ']]

                # [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', 'O', 'O', ' ', ' ', ' '],
                #           [' ', ' ', 'O', 'X', ' ', ' ', ' '],
                #           [' ', 'X', 'X', 'O', ' ', ' ', ' '],
                #           ['O', 'X', 'X', 'X', 'O', ' ', ' ']] # This example motivated checking singleMoveWins > 1 in utility


                # [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                #           [' ', ' ', ' ', 'O', ' ', ' ', ' '],
                #           [' ', ' ', 'X', 'X', ' ', ' ', ' ']] # This example motivated checking singleMoveWins > 1 in utility


            #[[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          #[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                          #[' ', ' ', 'X', ' ', ' ', ' ', ' '],
                          #[' ', ' ', 'O', 'X', ' ', ' ', ' '],
                          #[' ', ' ', 'X', 'O', 'X', ' ', ' '],
                          #[' ', ' ', 'O', 'X', 'O', ' ', ' ']] # This example motivated single moves to win utility


            #[['O', 'X', ' ', ' ', ' ', ' ', ' '],
                          #['X', 'X', 'X', ' ', ' ', ' ', ' '],
                          #['X', 'O', 'O', ' ', ' ', ' ', ' '],
                          #['X', 'O', 'X', ' ', ' ', ' ', ' '],
                          #['O', 'X', 'O', 'O', 'O', ' ', ' '],
                          #['X', 'X', 'O', 'O', 'X', 'O', ' ']]
            self.player = 'X'
        self.playerLookAHead = self.player # Next player to move
        self.movesExplored = 0 # Counter for number of moves explored
        self.winningValue = 1000 # Winning move number when negamax searching -- 4 in a row

    # Returns actual row object, not pointer
    def getRow(self, rowNum):
        if rowNum > 5 or rowNum < 0:
            raise ValueError(str(rowNum) + ' not a valid getRow request!')
        else:
            return self.board[rowNum]

    # Returns new object, copy of that column
    def getCol(self, colNum):
        if colNum > 6 or colNum < 0:
            raise ValueError(str(colNum) + ' not a valid getCol request!')
        else:
            boardColumns = [list(x) for x in zip(*self.board)]
            return boardColumns[colNum]

    # Returns the number of pieces in the board
    def locations(self, c):
        numberP = 0
        for row in self.board:
            numberP += row.count(c)
        return numberP

    # Returns columns that are not full
    def getMoves(self):
        moves = []
        index = 0
        for spot in self.board[0]:
            if spot is ' ':
                moves.append(index)
            index += 1
        return moves

    # Returns information on the state of the board:
    #   1 = a player has won and is next up
    #   -1 = a player has won and not next up
    #   0 = game is a draw, no one wins
    #   None if the game is still being played
    def getUtility(self):
        won, winner = self.isWon()
        if winner is 'X':
            # If X has won and is the next player to move, return 1
            # If X has won but is not the next player to move, return -1
            return 1000 if self.playerLookAHead is 'X' else -1000
        elif winner is 'O':
            # If O has won and is the next player to move, return 1
            # If O has won but is not the next player to move, return -1
            return 1000 if self.playerLookAHead is 'O' else -1000
        elif self.isFull():
            # If there is a draw (Cats game) return 0
            return 0
        else:
            # If the game is still being played, return bestIAR X - bestIAR O
            # ADDED SINGLE MOVE WINS.  A single move win adds 10 to respective bestIAR
            bestX = self.bestIAR_All('X')
            if debug: print('Best IAR X:', bestX)
            singleMoveWinsX = self.singleMoveWinCount('X')
            if debug: print('Single moves to win X:', singleMoveWinsX)
            # if 5 > singleMoveWinsX > 1: # There is 2 or more moves X can make to win.
                # return 500 if self.playerLookAHead is 'X' else -500
                # singleMoveWinsX = 5
            bestX += singleMoveWinsX * 10

            bestO = self.bestIAR_All('O')
            if debug: print('Best IAR O:', bestO)
            singleMoveWinsO = self.singleMoveWinCount('O')
            if debug: print('Single moves to win O:', singleMoveWinsO)
            # if 5 > singleMoveWinsO > 1: # There is 2 or more moves O can make to win.
                # return 500 if self.playerLookAHead is 'O' else -500
                # singleMoveWinsO = 5
            bestO += singleMoveWinsO * 10

            if singleMoveWinsX > 1 and singleMoveWinsO < 2:  # There is 2 or more moves X can make to win.
                return 500 if self.playerLookAHead is 'X' else -500
            if singleMoveWinsO > 1 and singleMoveWinsX < 2:  # There is 2 or more moves X can make to win.
                return 500 if self.playerLookAHead is 'O' else -500

            best = bestX - bestO
            # print('bestX {} bestO {}'.format(bestX, bestO))
            return best if self.playerLookAHead is 'X' else (best*-1)

    # Returns True if game is over, False otherwise
    def isOver(self):
        winBoo,_ = self.isWon()
        return winBoo

    # Puts the current player's mark at the column index passed.  DOESNT CHECK TO MAKE SURE THAT MOVE IS VALID...
    # Changes playerLookAhead because the next move is going to be made by the other player
    def makeMove(self, move):
        if move not in self.getMoves():
            raise ValueError(str(move) + ' not a valid column to make move!')
        global debug
        # Get row index to put piece
        currCol = self.getCol(move)
        blanks = [i for i, mark in enumerate(currCol) if mark == ' ']
        rowIndex = max(blanks)
        # Place piece in column
        self.board[rowIndex][move] = self.playerLookAHead
        # if debug: print('MADE MOVE {} @ ROW {} COL {}'.format(self.playerLookAHead, rowIndex, move))
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        # if debug: print('CHANGED NEXT UP TO:', self.playerLookAHead)
        self.movesExplored += 1

    # Changes player.  Also changes playerLookAHead because the new player hasnt made move yet so they are next up
    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player
        global debug
        # if debug: print('CHANGED PLAYER TO:', self.player)

    # Sets player and player look ahead.  Idk if this is the best way to do this...
    def setPlayer(self, piece):
        self.player = piece
        self.playerLookAHead = self.player

    # Removes mark from index passed and restores playerLookAHead b/c that move was taken back
    def unmakeMove(self, move):
        global debug
        # Get row index to remove piece
        currCol = self.getCol(move)
        # if debug: print('unmakeMove currCol:', currCol)
        if ' ' not in currCol:
            rowIndex = 0
        else:
            blanks = [i for i, mark in enumerate(currCol) if mark == ' ']
            # if debug: print('unmakeMove blanks:', blanks)
            rowIndex = max(blanks) + 1 if blanks is not None else 0

        if rowIndex > 5:
            raise ValueError(str(move) + ' not a valid column to remove piece from!')
        # Remove piece in column
        self.board[rowIndex][move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        # if debug: print('UNMADE MOVE:', move)

    # Returns the number of moves explored
    def getNumberMovesExplored(self):
        return self.movesExplored

    # Returns the number representing a win when negamax searching
    def getWinningValue(self):
        return self.winningValue

    def isEmpty(self):
        for row in self.board:
            if not ''.join(row).isspace():
                return False
        return True

    def isFull(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    # Returns true and winner if won, false and ' ' otherwise
    def isWon(self):
        hBoo, hWinner = self.isHorzWin()
        if hBoo:
            return hBoo, hWinner
        vBoo, vWinner = self.isVertWin()
        if vBoo:
            return vBoo, vWinner
        duBoo, duWinner = self.isDiagUpWin()
        if duBoo:
            return duBoo, duWinner
        ddBoo, ddWinner = self.isDiagDownWin()
        if ddBoo:
            return ddBoo, ddWinner
        return False, ' '

    # Returns true and piece of 4IAR if list has 4 pieces in a row (IAR), false and ' ' otherwise
    def has4IAR(self, group):
        lookFor = ' '
        cons = 0
        for spot in group:
            if spot is lookFor:
                cons += 1
            else:
                lookFor = spot
                cons = 1
            if cons is 4 and lookFor is not ' ':
                return True, lookFor
        return False, ' '

    # Returns true and winner if there is 4 in a row in any horizontal position, false and ' ' otherwise
    def isHorzWin(self):
        for row in self.board:
            boo, winner = self.has4IAR(row)
            if boo:
                return True, winner
        return False, ' '

    # Returns true and winner if there is 4 in a row in any vertical position, false and ' ' otherwise
    def isVertWin(self):
        boardColumns = [list(x) for x in zip(*self.board)]
        for col in boardColumns:
            boo, winner = self.has4IAR(col)
            if boo:
                return True, winner
        return False, ' '

    # Returns true and winner if there is 4 in a row in any diagonal up position, false and ' ' otherwise
    def isDiagUpWin(self):
        for du in self.getDiagUp():
            boo, winner = self.has4IAR(du)
            if boo:
                return True, winner
        return False, ' '

    # Returns true and winner if there is 4 in a row in any diagonal down position, false and ' ' otherwise
    def isDiagDownWin(self):
        for dd in self.getDiagDown():
            boo, winner = self.has4IAR(dd)
            if boo:
                return True, winner
        return False, ' '

    # returns diagonal up lists of board
    def getDiagUp(self):
        up = []
        grab = []
        rowStarti = 3
        rowi = 3
        coli = 0
        while rowStarti < 6:
            grab.append(self.board[rowi][coli])
            if rowi is 0:
                rowStarti += 1
                rowi = rowStarti
                coli = 0
                up.append(grab)
                grab = []
            else:
                rowi -= 1
                coli += 1
        grab = []
        colStarti = 1
        rowi = 5
        coli = 1
        while colStarti < 4:
            grab.append(self.board[rowi][coli])
            if coli is 6:
                colStarti += 1
                coli = colStarti
                rowi = 5
                up.append(grab)
                grab = []
            else:
                rowi -= 1
                coli += 1
        return up

    # returns diagonal down lists of board
    def getDiagDown(self):
        down = []
        grab = []
        rowStarti = 2
        rowi = 2
        coli = 0
        while rowStarti >= 0:
            grab.append(self.board[rowi][coli])
            if rowi is 5:
                rowStarti -= 1
                rowi = rowStarti
                coli = 0
                down.append(grab)
                grab = []
            else:
                rowi += 1
                coli += 1
        grab = []
        colStarti = 1
        rowi = 0
        coli = 1
        while colStarti < 4:
            grab.append(self.board[rowi][coli])
            if coli is 6:
                colStarti += 1
                coli = colStarti
                rowi = 0
                down.append(grab)
                grab = []
            else:
                rowi += 1
                coli += 1
        return down

    ########################################################################################################
    # Best in a row stuff

    # Returns the best overall best in a row for given piece on given board.  Wont ever be more than 4
    def bestIAR_All(self, piece):
        if debug: print('IN bestIAR_ALL FOR', piece)
        hBIAR = 0
        for row in self.board:
            hBIAR = max(hBIAR, self.bestIAR(row, piece))
        if debug: print('\tBest Horizontal:', hBIAR)
        hBIAR = hBIAR ** 2

        vBIAR = 0
        boardColumns = [list(x) for x in zip(*self.board)]
        for col in boardColumns:
            vBIAR = max(vBIAR, self.bestIAR(col, piece))
        if debug: print('\tBest Vertical:', vBIAR)
        vBIAR = vBIAR ** 2

        duBIAR = 0
        for u in self.getDiagUp():
            duBIAR = max(duBIAR, self.bestIAR(u, piece))
        if debug: print('\tBest Diag Up:', duBIAR)
        duBIAR = duBIAR ** 2

        ddBIAR = 0
        for d in self.getDiagDown():
            ddBIAR = max(ddBIAR, self.bestIAR(d, piece))
        if debug: print('\tBest Diag Down:', ddBIAR)
        ddBIAR = ddBIAR ** 2

        # overAllBest = max(hBIAR, vBIAR, duBIAR, ddBIAR)
        return hBIAR+vBIAR+duBIAR+ddBIAR #overAllBest if overAllBest < 4 else 4

    # Returns highest number of pieces ('piece') that could combine for a win for group (row, col, or diag)
    # EX: [' ', ' ', 'X', 'X', 'O', ' ', ' '] - Best X: 2, Best O: 0
    # EX: ['X', 'X', ' ', 'X', 'O', ' ', ' '] - Best X: 3, Best O: 0
    def bestIAR(self, group, piece):
        best = 0
        chunks = self.groupToChunks(group, piece)
        for chunk in chunks:
            best = max(best, chunk.count(piece))
        return best

    # Function gets chunks of potential win sets for piece
    # EX: group = [' ', ' ', 'X', 'X', 'O', ' ', ' '], piece = 'X' ==> [[' ', ' ', 'X', 'X']]
    # EX: group = [' ', 'X', 'X', 'O', 'O', ' ', ' '], piece = 'X' ==> []
    # EX: group = [' ', 'X', 'X', 'O', 'O', ' ', ' '], piece = 'O' ==> [['O', 'O', ' ', ' ']]
    def groupToChunks(self, group, piece):
        # Get indexs of piece or empty
        indexs = []
        for i, p in enumerate(group):
            if p in [piece, ' ']:
                indexs.append(i)

        # Get split indexs
        spl = [0] + [i for i in range(1, len(indexs)) if indexs[i] - indexs[i - 1] > 1] + [None]
        # print('spl:', spl)
        # List those index
        fin = [indexs[b:e] for (b, e) in [(spl[i - 1], spl[i]) for i in range(1, len(spl))]]
        # print('fin:', fin)
        # Indexs to elements from group
        grab = []
        for lst in fin:
            put = []
            for elm in lst:
                put.append(group[elm])
            # print('put:', put)
            if piece in put and len(put) >= 4: grab.append(put)
        return grab

    # Returns a count of single moves that would win for piece
    def singleMoveWinCount(self, piece):
        # print('IN SINGLE MOVES WIN COUNT WITH UTILITY {}'.format(self.getUtility()))
        # Save state of game
        PLAsave = self.playerLookAHead
        Psave = self.player
        self.setPlayer(piece)

        # Count single move wins
        singleMoveWinCounter = 0
        for m in self.getMoves():
            self.makeMove(m)
            # print('Move {} made utility {}'.format(m, self.getUtility()))
            if self.isWon()[0]:
                if debug: print('\tFOUND {}s WINNING MOVE {} IN SMWC'.format(piece, m))
                singleMoveWinCounter += 1
            # if self.singleMoveWinCount2(piece) > 1: # If there is two or more places you can move to win, youve won
            #     singleMoveWinCounter += 1
            self.unmakeMove(m)

        self.playerLookAHead = PLAsave
        self.player = Psave
        return singleMoveWinCounter

    # Returns a count of single moves that would win for piece.  Avoids recursion in SMWC
    def singleMoveWinCount2(self, piece):
        # print('IN SINGLE MOVES WIN COUNT WITH UTILITY {}'.format(self.getUtility()))
        # Save state of game
        PLAsave = self.playerLookAHead
        Psave = self.player
        self.setPlayer(piece)

        # Count single move wins
        singleMoveWinCounter = 0
        for m in self.getMoves():
            self.makeMove(m)
            # print('Move {} made utility {}'.format(m, self.getUtility()))
            if self.isWon()[0]:
                print('\tFOUND {}s WINNING MOVE {} IN SMWC2'.format(piece, m))
                singleMoveWinCounter += 1
            self.unmakeMove(m)

        self.playerLookAHead = PLAsave
        self.player = Psave
        return singleMoveWinCounter

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
