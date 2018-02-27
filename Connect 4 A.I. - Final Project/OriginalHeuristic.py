import C4Fast
import C4Helpers

# Returns the best overall best in a row for given piece on given board.  Wont ever be more than 4
def bestIAR_All(C4game, piece):
    # if debug: print('IN bestIAR_ALL FOR', piece)
    hBIAR = 0
    for row in C4game.board:
        hBIAR = max(hBIAR, bestIAR(row, piece))
    # if debug: print('\tBest Horizontal:', hBIAR)
    hBIAR = hBIAR ** 2

    vBIAR = 0
    boardColumns = [list(x) for x in zip(*C4game.board)]
    for col in boardColumns:
        vBIAR = max(vBIAR, bestIAR(col, piece))
    # if debug: print('\tBest Vertical:', vBIAR)
    vBIAR = vBIAR ** 2

    duBIAR = 0
    for u in C4game.getDiagUp():
        duBIAR = max(duBIAR, bestIAR(u, piece))
    # if debug: print('\tBest Diag Up:', duBIAR)
    duBIAR = duBIAR ** 2

    ddBIAR = 0
    for d in C4game.getDiagDown():
        ddBIAR = max(ddBIAR, bestIAR(d, piece))
    # if debug: print('\tBest Diag Down:', ddBIAR)
    ddBIAR = ddBIAR ** 2

    # overAllBest = max(hBIAR, vBIAR, duBIAR, ddBIAR)
    return hBIAR+vBIAR+duBIAR+ddBIAR #overAllBest if overAllBest < 4 else 4

# Returns highest number of pieces ('piece') that could combine for a win for group (row, col, or diag)
# EX: [' ', ' ', 'X', 'X', 'O', ' ', ' '] - Best X: 2, Best O: 0
# EX: ['X', 'X', ' ', 'X', 'O', ' ', ' '] - Best X: 3, Best O: 0
def bestIAR(group, piece):
    best = 0
    chunks = groupToChunks(group, piece)
    for chunk in chunks:
        best = max(best, chunk.count(piece))
    return best


# Function gets chunks of potential win sets for piece
# EX: group = [' ', ' ', 'X', 'X', 'O', ' ', ' '], piece = 'X' ==> [[' ', ' ', 'X', 'X']]
# EX: group = [' ', 'X', 'X', 'O', 'O', ' ', ' '], piece = 'X' ==> []
# EX: group = [' ', 'X', 'X', 'O', 'O', ' ', ' '], piece = 'O' ==> [['O', 'O', ' ', ' ']]
def groupToChunks(group, piece):
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
def singleMoveWinCount(C4game, piece):
    # if piece is not 'Z': return 0
    # print('IN SINGLE MOVES WIN COUNT WITH UTILITY {}'.format(self.getUtility()))
    # Save state of game
    # PLAsave = C4game.nextPiece
    # Psave = C4game.player
    # C4game.setPlayer(piece)
    # C4game.player = piece
    # C4game.nextPiece = C4game.player

    # if C4game.nextPiece is not piece:
    #     C4game.switchNextPiece

    # Save current next piece
    pieceSave = C4game.nextPiece
    C4game.nextPiece = piece
    # Count single move wins
    singleMoveWinCounter = 0
    for m in C4game.getMoves():
        C4game.makeMove(m)
        if C4game.isWon()[0]: singleMoveWinCounter += 1
        C4game.unmakeMove(m)
    C4game.nextPiece = pieceSave
    return singleMoveWinCounter




def utility(C4game):
    # If the game is still being played, return bestIAR X - bestIAR O
    # ADDED SINGLE MOVE WINS.  A single move win adds 10 to respective bestIAR
    bestX = bestIAR_All(C4game, 'X')
    # if debug: print('Best IAR X:', bestX)
    singleMoveWinsX = singleMoveWinCount(C4game, 'X')
    # if debug: print('Single moves to win X:', singleMoveWinsX)
    # if 5 > singleMoveWinsX > 1: # There is 2 or more moves X can make to win.
    # return 500 if self.playerLookAHead is 'X' else -500
    # singleMoveWinsX = 5
    bestX += singleMoveWinsX * 10

    bestO = bestIAR_All(C4game, 'O')
    # if debug: print('Best IAR O:', bestO)
    singleMoveWinsO = singleMoveWinCount(C4game, 'O')
    # if debug: print('Single moves to win O:', singleMoveWinsO)
    # if 5 > singleMoveWinsO > 1: # There is 2 or more moves O can make to win.
    # return 500 if self.playerLookAHead is 'O' else -500
    # singleMoveWinsO = 5
    bestO += singleMoveWinsO * 10

    if singleMoveWinsX > 1 and singleMoveWinsO < 2:  # There is 2 or more moves X can make to win.
        return 500 #if self.playerLookAHead is 'X' else -500
    if singleMoveWinsO > 1 and singleMoveWinsX < 2:  # There is 2 or more moves X can make to win.
        return -500 #if self.playerLookAHead is 'O' else -500

    best = bestX - bestO
    # print('bestX {} bestO {}'.format(bestX, bestO))
    return best #if self.playerLookAHead is 'X' else (best * -1)