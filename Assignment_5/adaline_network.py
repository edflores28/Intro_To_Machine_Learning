import random
import utilities

'''
This class performs the adaline network algorithm
'''


class Model:
    def __init__(self, train, test, total_classes, learn_rate=0.001):
        '''
        Initialization
        '''
        self.train = train
        self.test = test
        self.weights = []
        self.learn_rate = learn_rate
        self.total_classes = total_classes
        if total_classes <= 2:
            self.weights = [random.uniform(-1.0, 1.0) for i in range(len(train[0]))]
        else:
            for entry in range(total_classes):
                self.weights.append([random.uniform(-1.0, 1.0) for i in range(len(train[0]))])

    def __calculate(self, row):
        '''
        This class calculates the intermediate step for the
        weights update
        '''
        values = []
        # Create a temporary row and romove the classification
        temp = row[:-1]
        # Add a -1 for the bias weights
        temp.append(-1)
        # Multiply the weights and the row
        if self.total_classes <= 2:
            values = sum([a*b for a, b in zip(self.weights, temp)])
        # Otherwise multipy the weights and row for each class
        else:
            for entry in range(self.total_classes):
                values.append(sum([a*b for a, b in zip(self.weights[entry], temp)]))
        # Calculate the sum
        return values, temp

    def __calculate_weights(self, error):
        '''
        This method calculates the new weights
        '''
        temp = (self.learn_rate/len(error))*sum(error)
        if self.total_classes <= 2:
            self.weights = [self.weights[i] + temp for i in range(len(self.weights))]
        else:
            for entry in range(len(self.weights)):
                self.weights[entry] = [self.weights[entry][i] + temp for i in range(len(self.weights[entry]))]

    def __update_weights(self, total_errors):
        '''
        This method calculates the new weights
        '''
        # Iterate through each error
        if self.total_classes <= 2:
            for entry in total_errors:
                self.__calculate_weights(entry)
        # Otherwise iterate through each error for each class
        else:
            for label in range(self.total_classes):
                for entry in total_errors[label]:
                    self.__calculate_weights(entry)

    def train_model(self):
        '''
        This method trains the adaline network
        '''
        total_errors = []
        # Create additional entries for each class
        if self.total_classes > 2:
            total_errors = [[] for i in range(self.total_classes)]
        # Iterate through each row in the trianing set
        for row in self.train:
            # Calculate y and obtain the temporary row
            y, temp = self.__calculate(row)
            # Calculate the errors and append them to a list
            if self.total_classes <= 2:
                errors = [(row[-1]-y)*temp[i] for i in range(len(temp))]
                total_errors.append(errors)
            else:
                for entry in range(self.total_classes):
                    errors = [(row[-1]-y[entry])*temp[i] for i in range(len(temp))]
                    total_errors[entry].append(errors)
        # Perform the final update on the weights
        self.__update_weights(total_errors)

    def __predict(self, row):
        '''
        This method makes a prediction for the given row
        '''
        # Calvulate the value for the signum function
        summation, temp = self.__calculate(row)
        # Reutn the prediction
        if self.total_classes <= 2:
            return utilities.signum(summation)
        # Otherwise obtain the signum for each class and
        # return the class with 1.
        else:
            y = [utilities.signum(summation[i]) for i in range(len(summation))]
            indices = [i for i, x in enumerate(y) if x == 1]
            try:
                return (random.choice(indices))
            except IndexError:
                return random.randint(0, self.total_classes-1)

    def test_model(self):
        '''
        This method tests the trained model
        '''
        incorrect = 0
        summation, temp = self.__calculate(self.test[0])
        for row in self.test:
            pred = self.__predict(row)
            if pred != row[-1]:
                incorrect += 1
        return((incorrect*100)/len(self.test))
