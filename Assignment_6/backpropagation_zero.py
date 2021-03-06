import random
import utilities
import copy

MAX_EPOCH = 250
MAX_PRINT = 5
cprint = True


class Model:
    def __init__(self, train, test, outputs, learn_rate=0.001):
        '''
        Initialization
        '''
        self.train = train
        self.test = test
        self.validation = []
        # Pull 10% of the training set to use for early stopping
        for i in range(int(len(train)*.10)):
            self.validation.append(self.train.pop())
        self.learn_rate = learn_rate
        self.outputs = outputs
        self.weightsO = []
        # Create the weights for the output later including the bias
        for i in range(outputs):
            temp = [random.uniform(-1.0, 1.0) for i in range(len(train[0]))]
            self.weightsO.append(temp)

    def __forward_propagate(self, row):
        '''
        This method calculates all the node outputs for each
        layer in the network
        '''
        # Append a 1 to the row to account for the bias
        row = [1] + row[:-1]
        self.output = utilities.calculate_sigmoid_batch(self.weightsO, row, self.outputs)
        if cprint:
            print("Output later outputs")
            print(self.output[:MAX_PRINT], "\n")
            print("Forward propagation finished\n")

    def __backpropagate(self, row):
        '''
        This method propagates the error from the outputs back
        to the inputs and performs weight updates
        '''
        global cprint
        deltaO = []
        # Add a 1 to the row
        # to account for the bias weight
        t_row = [1] + row[:-1]
        # Create a list for expected values
        expected = utilities.create_expected(self.outputs, row)
        # Iterate through the outputs and calculate the
        # delta values
        for i in range(self.outputs):
            error = expected[i] - self.output[i]
            deltaO.append(utilities.calculate_derivative(self.output[i]) * error)
        # Iterate through the output nodes and
        # update their weights
        for i in range(self.outputs):
            temp = [self.learn_rate*t_row[j]*deltaO[i] for j in range(len(t_row))]
            self.weightsO[i] = [self.weightsO[i][j] + temp[j] for j in range(len(self.weightsO[i]))]
        if cprint:
            print("Output layer deltas")
            print(deltaO[:MAX_PRINT], "\n")
            print("Output layer new weights")
            print(self.weightsO[:MAX_PRINT], "\n")
            print("Back propagation finished\n")

    def train_model(self):
        '''
        This method calculates all the node outputs for each
        layer in the network
        '''
        global cprint
        prev_weightsO = []
        prev_correct = 0
        epoch = 0
        # Train the network until broken
        while True:
            # Iterate through all the rows
            for row in range(len(self.train)):
                # Calculate the outputs of each layer
                self.__forward_propagate(self.train[row])
                # Backpropagate the errors
                self.__backpropagate(self.train[row])
                if row == 5:
                    cprint = False
            # Determine the classification accuracy of the network
            correct = self.test_model(True)
            # If the correct value is less than previous
            # correct value or the epoch is greater than
            # the maximum epoch break the loop.
            if correct < prev_correct or epoch > MAX_EPOCH:
                # Restore the weights
                self.weightsO = prev_weightsO
                print("Finished training")
                print("Final accuracy with validation set:", correct)
                print("Total epochs:", epoch, "\n")
                break
            # Save the weights, the correct value
            # and increment the epoch
            prev_correct = correct
            prev_weightsO = copy.deepcopy(self.weightsO)
            epoch += 1

    def __predict(self, row):
        '''
        This method predicts the classification of the row
        '''
        self.__forward_propagate(row)
        return utilities.network_predict(self.output)

    def test_model(self, validate=False):
        '''
        This method tests the network
        '''
        correct = 0
        incorrect = 0
        test = self.test
        # Use the validation set if the flag is set
        if validate:
            test = self.validation
        # Iterate over each row
        for row in test:
            pred = self.__predict(row)
            if pred == row[-1]:
                correct += 1
            else:
                incorrect += 1
        return (correct*100)/(correct+incorrect)
