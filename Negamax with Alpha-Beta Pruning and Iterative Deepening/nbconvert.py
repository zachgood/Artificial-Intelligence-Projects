
# coding: utf-8

# # Assignment 4: Negamax with Alpha-Beta Pruning and Iterative Deepening

# Still being developed, but you may get started on this when you are finished with Assignment 3.

# # Table of Contents
# * [Assignment 4: Negamax with Alpha-Beta Pruning and Iterative Deepening](#Assignment-4:-Negamax-with-Alpha-Beta-Pruning-and-Iterative-Deepening)
# 	* [Initial Code](#Initial-Code)
# 	* [Add moves counter](#Add-moves-counter)
# 	* [negamaxIDS](#negamaxIDS)
# 	* [negamaxIDSab](#negamaxIDSab)
# 	* [Grading](#Grading)
# 	* [Extra Credit](#Extra-Credit)
# 

# For this assignment, you will investigate the advantages of alpha-beta
# pruning applied to Tic-Tac-Toe.  To do so, follow these steps.

# ## Initial Code <font color='red'>UPDATED Oct 8</font>

# In[1]:

def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    return bestValue, bestMove


# In[2]:

class TTT(object):

    def __init__(self):
        self.board = [' ']*9
        self.player = 'X'
        if False:
            self.board = ['X', 'X', ' ', 'X', 'O', 'O', ' ', ' ', ' ']
            self.player = 'O'
        self.playerLookAHead = self.player

    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        whereX = self.locations('X')
        whereO = self.locations('O')
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            return 0
        else:
            return None  ########################################################## CHANGED FROM -0.1

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s


# Check that the following function `playGame` runs
# correctly. Notice that we are using *negamax* to find the best move for
# Player X, but Player O, the opponent, is using function *opponent*
# that follows the silly strategy of playing in the first open position.

# In[3]:

def opponent(board):
    return board.index(' ')

def playGame(game,opponent,depthLimit):
    print(game)
    while not game.isOver():
        score,move = negamax(game,depthLimit)
        if move == None :
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)   ### FIXED ERROR IN THIS LINE!
            print(game)
            game.changePlayer()


# In[4]:

game = TTT()
playGame(game,opponent,20)


# ## Add moves counter

# Evaluate the efficiency of the search by keepting track of the number of nodes explored, which is the same as the number of moves explored, during a game. Do this by adding a counter named `movesExplored` to the `TTT` constructor where it is initialized to 0 and increment the counter in the `TTT.makeMove` method.  Add a method `ttt.getNumberMovesExplored()` to get its current value.  So
# 
#     print('Number of moves explored', game.getMovesExplored())
#     
# will print the number of moves explored. You will not use a global variable for counting this time.

# ## negamaxIDS 

# <font color='red'>UPDATED Oct 4</font>
# 
# Write a new function named `negamaxIDS` that performs an iterative deepening negamax search.  Replace the first line in the `while` loop of `playGame` with
# 
#         score,move = negamaxIDS(game,depthLimit)
#         
# where `depthLimit` is now the maximum depth and multiple `negamax` searches are performed for depth limits of $1, 2, \ldots,$ maximum depth.
# 
# But, when should you stop?  Can you stop before readhing the depthLimit?  If not, there is no point to doing iterative deepening.
# 
# For Tic-Tac-Toe, we can stop as soon as a call to `negamax` returns a winning move.  This will have a value of 1 for Tic-Tac-Toe.  To keep our `negamaxIDS` function general, add a method called `getWinningValue` to the `TTT` class that just returns 1.  Then `negamaxIDS` can call `game.getWinningValue()` to determine the value of a winning move for this game.  If the maximum depth is reached and no winning move has been found, return the best move found over all depth limts.

# ## negamaxIDSab

# Now for the hardest part.  Make a new function `negamaxIDSab` by duplicating `negamaxIDS` and add the code to implement alpha-beta pruning.

# ## playGames
# 
# Now duplicate the game playing loop so three complete tic-tac-toe games are played.  Call this new version `playGames`. For the first game, use `negamax`. For the second game, use `negamaxIDS`.  For the third game, use `negamaxIDSab`.  At the end of each game, print the number of X's in the final board, the number moves explored, the depth of the game which is the number of moves made by X and O, and the effective branching factor.  When you run `playGames` you should see the tic-tac-toe positions after each move and, after all games are done, a line for each game like the following lines, which were <font color='red'>UPDATED Oct 8</font>.
# 
#     negamax made 4 moves. 558334 moves explored for ebf(558334, 7) of 6.46
#     negamaxIDS made 3 moves. 23338 moves explored for ebf(23338, 5) of 7.26
#     negamaxIDSab made 3 moves 6053 moves explored for ebf(6053, 5) of 5.48
# 
# Your results may be different. 
# 
# The value of the depth is the total number of moves made by X and by O during the search.  You can calculate this by keeping a list of all board states, or by just counting the number of X's and O's in the final board.

# Here are some example results. <font color='red'>Updated October 8, 3:15pm </font>

# In[8]:

playGames(opponent, 10)


# ## Grading

# As always, download and extract from [A4grader.tar](http://www.cs.colostate.edu/~anderson/cs440/notebooks/A4grader.tar)

# In[9]:

get_ipython().magic('run -i A4grader.py')


# ## Extra Credit 

# Earn one extra credit point for each of the following.
# 
#   - Implement another game and repeat the above steps.
# 
#   - Implement a random move chooser as the opponent (Player O) and determine how many times Player X can win against this opponent as an average over multiple games.

# In[ ]:




# coding: utf-8

# # Assignment 4: Negamax with Alpha-Beta Pruning and Iterative Deepening

# ### Zach Goodenow
# 10/11/17
# <br>
# CS 440

# Still being developed, but you may get started on this when you are finished with Assignment 3.

# # Table of Contents
# * [Assignment 4: Negamax with Alpha-Beta Pruning and Iterative Deepening](#Assignment-4:-Negamax-with-Alpha-Beta-Pruning-and-Iterative-Deepening)
# 	* [Initial Code](#Initial-Code)
# 	* [Add moves counter](#Add-moves-counter)
# 	* [negamaxIDS](#negamaxIDS)
# 	* [negamaxIDSab](#negamaxIDSab)
# 	* [Grading](#Grading)
# 	* [Extra Credit](#Extra-Credit)
# 

# For this assignment, you will investigate the advantages of alpha-beta
# pruning applied to Tic-Tac-Toe.  To do so, follow these steps.

# ## Initial Code

# I replaced `negamax`, `TTT`, `opponent`, and `playGame` with my edits here...

# In[5]:

debug = False

# Returns the best move for the current state of the game and the value associated
def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue = -float('infinity')
    bestMove = None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        # Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        if debug: print('\tDepth {}, Value {}, Move {}, Player {}'.format(depthLeft, value, move, game.playerLookAHead))
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move
    return bestValue, bestMove


# In[6]:

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

    # Returns information on the state of the board:
    #   1 = a player has won and is next up
    #   -1 = a player has won and not next up
    #   0 = game is a draw, no one wins
    #   None if the game is still being played
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
        self.movesExplored += 1

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


# Check that the following function `playGame` runs
# correctly. Notice that we are using *negamax* to find the best move for
# Player X, but Player O, the opponent, is using function *opponent*
# that follows the silly strategy of playing in the first open position.

# In[7]:

# A dumby opponent
def opponent(board):
    return board.index(' ')

def playGame(game,opponent,depthLimit, algorithm = negamax):
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


# In[8]:

game = TTT()
playGame(game,opponent,10)


# The above results are interesting b/c the third move for 'X' made my `negamax` was 4 not 6.  6 would have ended the game in a win but 4 insures a win.  Why not just win?

# ## negamaxIDS 

# <font color='red'>UPDATED Oct 4</font>
# 
# Write a new function named `negamaxIDS` that performs an iterative deepening negamax search.  Replace the first line in the `while` loop of `playGame` with
# 
#         score,move = negamaxIDS(game,depthLimit)
#         
# where `depthLimit` is now the maximum depth and multiple `negamax` searches are performed for depth limits of $1, 2, \ldots,$ maximum depth.
# 
# But, when should you stop?  Can you stop before readhing the depthLimit?  If not, there is no point to doing iterative deepening.
# 
# For Tic-Tac-Toe, we can stop as soon as a call to `negamax` returns a winning move.  This will have a value of 1 for Tic-Tac-Toe.  To keep our `negamaxIDS` function general, add a method called `getWinningValue` to the `TTT` class that just returns 1.  Then `negamaxIDS` can call `game.getWinningValue()` to determine the value of a winning move for this game.  If the maximum depth is reached and no winning move has been found, return the best move found over all depth limts.

# <div class="alert alert-block alert-info">
# *negamaxIDS* basically just runs *negamax* with *maxdepth* increasing.
# 
# For every depth, it updates *bestValue* and *bestMove*.  
# 
# **The key here** is that it early returns if value is game winning value.  Otherwise, it wouldn't be any more useful than just running *negamax* with maxDepth.  This is an attempt to optimize nodes searched because you could find the best move at a depth way before maxDepth.

# In[9]:

debug = False

# Performs an iterative deepening negamax search.  Returns best move for current state and value assosicated
def negamaxIDS(game, maxDepth):
    global debug
    bestValue = -float('infinity')
    bestMove = None
    # bestMove = game.getMoves()[0]
    for depth in range(maxDepth+1):
        value, move = negamax(game, depth)
        # Should I check for failure??????????????????????????
        # Why would negamax return infinity???????????????????
        if value in {None, float('Inf')}: # removed-> , -float('Inf')
            if debug: print('***Depth {} found {} for move {}'.format(depth, value, move))
            continue
        if value is game.getWinningValue(): # Found winning move, so return it
            if debug: print('Found winning value at depth {} with move {}'.format(depth, move))
            return value, move
        if value > bestValue: # Found a new best move
            bestValue = value
            bestMove = move
        if debug:
            print('Depth {} has value {} for move {}'.format(depth, value, move))
            print('AND BestValue {} for BestMove {}'.format(bestValue, bestMove))
    return bestValue, bestMove


# ## negamaxIDSab

# Now for the hardest part.  Make a new function `negamaxIDSab` by duplicating `negamaxIDS` and add the code to implement alpha-beta pruning.
# <br><br>
# **From Negamax notes:** <br>
# Modify Negamax to perform alpha-beta cutoffs by making these changes:
# - Two new arguments, `alpha` and `beta`, whose initial values are −∞ and ∞.
# - In the for loop for trying moves, negate and swap the values of `alpha` and `beta`, and the returned value from recursive calls must be negated.
# - Do early return if `bestScore` is greater than or equal to `beta`.
# - Update `alpha` to maximum of `bestScore` and current `alpha`.

# <div class="alert alert-block alert-info">
# I applyed the bullet points above to *negamax* to make the function *negamaxab*.
# 
# *negamaxIDSab* : *negamaxab* = *negamaxIDS* : *negamax*
# 
# Dificulty was figuring out where/when to prune.  I was also switching and negating alpha and beta in the for loop when this should be occuring before exploring children nodes.
# 
# What I learned was that pruneing is helpful because if you find a move better than your opponents best move, it is garenteed to be a good move so you dont have to explore other options.  
# 

# This is the basic outline I have learned for recursive search functions:
# 
# **define function**
#     1. Check base case and return if true
#     2. Assign values that are equivalent for all child nodes will need
# **loop through all children and...**
#     3. Apply anything needed for traversing DOWN a child/node tree
# **make recursive call**
#     4. Check problem/useless values and take corrasponding action
#     5. Apply anything needed for traversing UP a child/node tree

# In[10]:

debug = False

# negamaxIDS but with alpha beta pruning
def negamaxIDSab(game, maxDepth, alpha = -float('Inf'), beta = float('Inf')):
    global debug
    bestValue = -float('infinity')
    bestMove = None
    # bestMove = game.getMoves()[0]
    for depth in range(maxDepth + 1):
        value, move = negamaxab(game, depth)
        # Should I check for failure??????????????????????????
        # Why would negamax return infinity???????????????????
        if value in {None, float('Inf')}:  # removed-> , -float('Inf')
            if debug: print('***Depth {} found {} for move {}'.format(depth, value, move))
            continue
        if value is game.getWinningValue():  # Found winning move, so return it
            if debug: print('Found winning value at depth {} with move {}'.format(depth, move))
            return value, move
        if value > bestValue:  # Found a new best move
            bestValue = value
            bestMove = move
        if debug:
            print('Depth {} has value {} for move {}'.format(depth, value, move))
            print('AND BestValue {} for BestMove {}'.format(bestValue, bestMove))
    return bestValue, bestMove


# Negamax search but with alpha beta pruning
def negamaxab(game, depthLeft, alpha = -float('Inf'), beta = float('Inf')):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue = -float('infinity')
    bestMove = None
    # Swap and negate alpha beta
    alpha, beta = -beta, -alpha
    if debug:
        print('{}\n^Game in ngmxAB -> Depth Left: {}, alpha: {}, beta: {}'.format(game, depthLeft, alpha, beta))
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)

        # Use depth-first search to find eventual utility value and back it up.
        value, _ = negamaxab(game, depthLeft - 1, alpha, beta)

        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue

        # Negate it because it will come back in context of next player
        value = - value
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move

        # Update alpha to maximum of bestScore and current alpha
        alpha = max(bestValue, alpha)


        if debug:
            print('\tmove {} has value: {}, alpha: {}, beta: {}, bestValue: {}, bestMove: {}'.format(move, value, alpha, beta, bestValue, bestMove))

        # Do early return if bestScore is greater than or equal to beta
        if bestValue >= beta:
            if debug: print('\t*PRUNE FOUND* move {}. bestValue: {}, beta: {}, bestMove: {}'.format(move, bestValue, beta, bestMove))
            return bestValue, bestMove

    return bestValue, bestMove


# ## playGames
# 
# Now duplicate the game playing loop so three complete tic-tac-toe games are played.  Call this new version `playGames`. For the first game, use `negamax`. For the second game, use `negamaxIDS`.  For the third game, use `negamaxIDSab`.  At the end of each game, print the number of X's in the final board, the number moves explored, the depth of the game which is the number of moves made by X and O, and the effective branching factor.  When you run `playGames` you should see the tic-tac-toe positions after each move and, after all games are done, a line for each game like the following lines, which were <font color='red'>UPDATED Oct 5</font>.
# 
#     negamax made 4 moves. 558334 moves explored for ebf(558334, 7) of 6.46
#     negamaxIDS made 3 moves. 744695 moves explored for ebf(744695, 5) of 14.73
#     negamaxIDSab made 3 moves 20804 moves explored for ebf(20804, 5) of 7.09
# 
# Your results may be different. 
# 
# The value of the depth is the total number of moves made by X and by O during the search.  You can calculate this by keeping a list of all board states, or by just counting the number of X's and O's in the final board.

# Since `playGames` uses `ebf`, define an `ebf` function from A3. 
# <br><br>
# I actually used the code that Dr. Anderson posted on piazza for `ebf` to insure I have the same values.

# In[13]:

def ebf(nNodes, depth, precision=0.01):
    if nNodes == 0:
        return 0

    def ebfRec(low, high):
        mid = (low + high) * 0.5
        if mid == 1:
            estimate = 1 + depth
        else:
            estimate = (1 - mid**(depth + 1)) / (1 - mid)
        if abs(estimate - nNodes) < precision:
            return mid
        if estimate > nNodes:
            return ebfRec(low, mid)
        else:
            return ebfRec(mid, high)

    return ebfRec(1, nNodes)


# In[14]:

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


# Here are some example results.

# In[15]:

playGames(opponent, 10)


# Here are some example results. Updated October 6, 3:15pm

# ## Grading

# As always, download and extract from [A4grader.tar](http://www.cs.colostate.edu/~anderson/cs440/notebooks/A4grader.tar)

# In[7]:

# from A4mysolution import *


# In[8]:

get_ipython().magic('run -i A4grader.py')


# ## Extra Credit 

# Earn one extra credit point for each of the following.
# 
#   - Implement another game and repeat the above steps.
# 
#   - Implement a random move chooser as the opponent (Player O) and determine how many times Player X can win against this opponent as an average over multiple games.

# In[1]:

import numpy as np
maze = np.array(mazelist).view('U1').reshape((len(mazelist), len(mazelist[0])))
print(maze.shape)
maze[::-1,:]


# In[3]:

w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)] 
Matrix


# In[8]:

c4board = [[' ' for x in range(7)] for y in range(6)] 
c4board


# In[27]:

c4board[5][0] = 1
c4board[5][1] = 0
c4board[4][0] = 1
c4board[4][1] = 1
c4board[3][2] = 1
c4board


# In[28]:

print('we have .{}.'.format(c4board[5][0]))


# In[26]:

oth = np.where(c4board == 'X')
for o in oth: 
    print(o)


# In[20]:

zp = zip(*np.where(c4board == 'O'))
for z in zp: 
    print(z)


# In[ ]:



