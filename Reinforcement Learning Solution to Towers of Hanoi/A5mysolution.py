from Hanoi import *
import numpy as np
import random


# To slowly transition from taking random actions to taking the action currently believed to be best,
# called the greedy action, we slowly decay a parameter, ϵ,
# from 1 down towards 0 as the probability of selecting a random action.
# This is called the ϵ -greedy policy.
def epsilonGreedy(epsilon, Q, state, validMovesF):
    debug = False
    validMoves = (validMovesF(state))
    if np.random.uniform() < epsilon: # Random move
        randomMove = random.choice(validMoves)
        if debug:
            print('epsilonGreedy chose random move')
            print('\tValid moves are',validMoves)
            print('\tRandom move:', randomMove)
        return randomMove
    else: # Greedy Move
        # get Q values for all validMoves
        Qs = np.array([Q.get(stateMoveTuple(state,  m), 0) for m in validMoves])
        # get move with largest Q value
        # bestMove = validMoves[np.argmax(Qs)] # argmax returns index of max value
        bestMove = validMoves[np.argmin(Qs)]  # argmin returns index of min value
        if debug:
            print('epsilonGreedy chose greedy mvoe')
            print('\tValid moves are', validMoves)
            print('\tQ values for validMoves are', Qs)
            print('\tBest move is', bestMove)
        return bestMove


# train the Q function for number of repetitions, decaying epsilon at start of each repetition.
# Returns Q and list or array of number of steps to reach goal for each repetition.
def trainQ(nRepetitions, learningRate, epsilonDecayFactor, validMovesF, makeMoveF, numRings = 3, numProngs = 3):
    # Set up Q table
    Q = {}  # empty dict to keep track of temporal difference error for each state, move pair
    stepsToGoal = np.zeros(nRepetitions) # To keep track of number steps to success for each game played
    outcomes = np.zeros(nRepetitions) # To keep track of the outcome of each game played.  I DONT THINK THIS IS USEFUL FOR HANOI
    epsilons = np.zeros(nRepetitions) # To keep track of the epsilon value for each game played

    # Start epislon at 1 and decay every step
    epsilon = 1.0
    graphics = False
    showMoves = not graphics
    showMoves = False

    # if graphics:
    #     fig = plt.figure(figsize=(10, 10))


    # This loop is to play the game nRepetitions times
    for nRep in range(nRepetitions):
        epsilon *= epsilonDecayFactor # Update epsilon
        epsilons[nRep] = epsilon # Keep track of epilon for each game played
        step = 0 # Keep track of how many steps each game takes
        # state = [[1, 2, 3], [], []] # Set up starting state
        # state = [[1, 2, 3, 4], [], []] # Set up starting state with 4 disks
        # state = [[1, 2, 3, 4, 5], [], []] # Set up starting state with 5 disks
        # state = [list(range(1, numRings + 1)), [], []]
        state = np.empty((numProngs, 0)).tolist() # get numProngs lists in a list
        state[0] = list(range(1, numRings + 1)) # Add numRings ints to first prong/list
        done = False

        if nRep % 50 == 0:
            print('Starting rep number {} with epsilon {} and prev steps2goal {}'.format(nRep, epsilon, stepsToGoal[nRep-1]))

        # This loop is to play the game once and update Q accordingly
        while not done:
            # Pick move depending on weight of epsilon and values of Q
            move = epsilonGreedy(epsilon, Q, state, validMovesF)

            stamp = stateMoveTuple(state, move) # Stamp the state and move for key in Q
            newState = makeMoveF(state, move) # Apply the move and save resulting state
            step += 1

            # If the state move tuple isnt in Q yet, give it -1 and update later
            if stamp not in Q:
                Q[stamp] = 1 # OR SHOULD THIS BE 0?!?!?!
            if showMoves:
                printState(newState)

            # If move resulted in win, update Q to reflect
            if winner(newState):
                if showMoves:
                    print('       Game Won with {} steps!'.format(step))
                Q[stamp] = 1
                done = True
                stepsToGoal[nRep] = step
                outcomes[nRep] = 1

            # if not a win, calculate the temporal difference error
            # use it to adjust the Q value of the previous state, move.
            # We do this only if we are not at the first move of a game. WHY? b/c no previous state, move on first move
            if step > 1:
                Q[oldStamp] += learningRate * (1 + Q[stamp] - Q[oldStamp])

            # Q(oldstate, oldmove) = Q(oldstate, oldmove) + learningrate * (-1 + Q(state, move) - Q(oldstate, oldmove)

            # Set up for next move:
            # Save current state, move as old state, move so Q(state, move) can be updated after next steps
            oldState, oldMove = state, move
            # Stamp old state, move.
            oldStamp = stateMoveTuple(oldState, oldMove)
            # Take next step for state
            state = newState
    print(epsilons)
    return Q, stepsToGoal



# without updating Q, use Q to find greedy action each step until goal is found. Return path of states.
def testQ(Q, maxSteps, validMovesF, makeMoveF, numRings = 3, numProngs = 3):
    epsilon = 0 # Because we dont want any random moves
    step = 0  # Keep track of how many steps each game takes
    # state = [[1, 2, 3], [], []]  # Set up starting state
    # state = [[1, 2, 3, 4], [], []]  # Set up starting state with 4 disks
    # state = [[1, 2, 3, 4, 5], [], []]  # Set up starting state with 5 disks
    # state = [list(range(1, numRings + 1)), [], []]
    state = np.empty((numProngs, 0)).tolist()  # get numProngs lists in a list
    state[0] = list(range(1, numRings + 1))  # Add numRings ints to first prong/list
    path = [] # To keep track of the steps and states taken

    # Play the game until done
    while step <= maxSteps:
        # Put the state in the path
        path.append(state)
        # Check completion
        if winner(state):
            break
        step += 1
        # use Q to find greedy action
        move = epsilonGreedy(epsilon, Q, state, validMovesF)
        # make the move
        state = makeMoveF(state, move)

    return path


if __name__ == '__main__':
    rings = 4
    prongs = 4
    Q, stepsToGoal = trainQ(200, 0.5, 0.7, validMoves, makeMove, rings, prongs)
    # Q, stepsToGoal = trainQ(50, 0.95, 0.5, validMoves, makeMove)
    # for elm in Q:
    #     print(elm, "-->", Q.get(elm))

    # train info
    print(stepsToGoal)
    minSteps = min(stepsToGoal)
    times = sum(stepsToGoal == minSteps)
    print('lowest steps `{}` found `{}` times'.format(minSteps, times))

    # Test test
    path = testQ(Q, 100, validMoves, makeMove, rings, prongs)
    for s in path:
        printState(s)
        print()
    # printState(path[-3])
    # printState(path[-2])
    # printState(path[-1])
    print('It took {} steps to win this puzzle'.format(len(path)-1))




    state = [[1,2,3], [], []]
    Q = {}  # empty table
    # Checking epsilon greedy is working
    # epsilonGreedy(0.8, Q, state, validMoves)

