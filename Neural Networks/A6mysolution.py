import numpy as np
import mlutils as ml
import neuralnetworks as nn
import time
import scaledconjugategradient as scg



# returns a list of lists like results
# but with the list of training performances replaced by their mean
# and the list of testing performances replaced by their mean
def summarize(results):
    sumz = []
    for layer in results: #range(len(results)/3):
        sumz.append([layer[0], np.mean(layer[1]), np.mean(layer[2]), layer[3]])
    return sumz


# takes the output of summarize(results) and returns the best element of results,
# determined by the element that has the smallest test performance.
def bestNetwork(summary):
    bestNet = [-1]
    smallestTestP = float('inf')
    for layer in summary:
        if layer[2] < smallestTestP:
            smallestTestP = layer[2]
            bestNet = layer
    return bestNet


# Helper when not a classify problem
def performance(X, T, trainFraction, hidden, numberRepetitions, numberIterations):
    # Make the lists for train and test data performance
    trainP = []
    testP = []

    # For numberRepetitions
    for rep in range(numberRepetitions):
        # Use ml.partition to randomly partition X and T into training and testing sets.
        Xtrain, Ttrain, Xtest, Ttest = ml.partition(X, T, (trainFraction, 1 - trainFraction), classification=False)

        # Create a neural network of the given structure
        nnet = nn.NeuralNetwork(X.shape[1], hidden, T.shape[1])

        # Train it for numberIterations
        # nnet.train(X, T, numberIterations)
        nnet.train(Xtrain, Ttrain, numberIterations)

        # Use the trained network to produce outputs for the training and for the testing sets
        Ytrain = nnet.use(Xtrain)
        Ytest = nnet.use(Xtest)

        # Calculate the RMSE of training and testing sets.
        trainRMSE = np.sqrt(np.mean((Ytrain - Ttrain) ** 2))
        testRMSE = np.sqrt(np.mean((Ytest - Ttest) ** 2))

        # Add the training and testing performance to a collection (such as a list) for this network structure
        trainP.append(trainRMSE)
        testP.append(testRMSE)

    # Return trainP and testP
    return trainP, testP


# Helper when classify problem
def performanceC(X, T, trainFraction, hidden, numberRepetitions, numberIterations):
    # Make the lists for train and test data performance
    trainP = []
    testP = []

    # For numberRepetitions
    for rep in range(numberRepetitions):
        # Use ml.partition to randomly partition X and T into training and testing sets.
        Xtrain, Ttrain, Xtest, Ttest = ml.partition(X, T, (trainFraction, 1 - trainFraction), classification=True)

        # Create a neural network of the given structure
        nnet = nn.NeuralNetworkClassifier(X.shape[1], hidden, len(np.unique(T)))

        # Train it for numberIterations
        # nnet.train(X, T, numberIterations)
        nnet.train(Xtrain, Ttrain, numberIterations)

        # Use the trained network to produce outputs for the training and for the testing sets
        Ytrain = nnet.use(Xtrain)
        Ytest = nnet.use(Xtest)

        # Calculate the fraction of samples incorrectly classified for training and testing sets
        trainFrac = np.sum(Ytrain != Ttrain) / Ttrain.shape[0]
        testFrac = np.sum(Ytest != Ttest) / Ttest.shape[0]

        # Add the training and testing performance to a collection (such as a list) for this network structure
        trainP.append(trainFrac)
        testP.append(testFrac)

    # Return trainP and testP
    return trainP, testP


# This function returns results which is a list with one element for each network structure tested
def trainNNs(X, T, trainFraction, hiddenLayerStructures, numberRepetitions, numberIterations, classify):
    results = []
    # For each network structure given in hiddenLayerStructures
    for hidden in hiddenLayerStructures:
        # Make the element for this structure
        element = [hidden]

        # Clock the time
        startTime = time.time()

        # Get preformance
        args = [X, T, trainFraction, hidden, numberRepetitions, numberIterations]
        trainP, testP = performanceC(*args) if classify else performance(*args)

        # Add to a collection of all results the hidden layer structure,
        # lists of training performance and testing performance,
        element.append(trainP)
        element.append(testP)
        # and seconds taken to do these repetitions.
        element.append(time.time() - startTime)

        # add the element for this hidden layer structure to results
        results.append(element)
    # return the collection of all results
    return results


if __name__ == '__main__':
    print('hello world')
    X = np.arange(10).reshape((-1, 1))
    T = X + 1 + np.random.uniform(-1, 1, ((10, 1)))


    #results = trainNNs(X, T, 0.8, [2, 10, [10, 10]], 5, 100, classify=False)
    results = trainNNs(X, T, 0.8, [0, 1, 2, 10, [10, 10], [5, 5, 5, 5], [2] * 5], 50, 400, classify=False)
    print(results)

    for sumz in summarize(results):
        print(sumz)

    best = bestNetwork(summarize(results))
    print(best)
    print('Hidden Layers {} Average RMSE Training {:.2f} Testing {:.2f} Took {:.2f} seconds'.format(*best))


    # results = trainNNs(X, T, trainFraction, hiddenLayerStructures, numberRepetitions, numberIterations, classify)