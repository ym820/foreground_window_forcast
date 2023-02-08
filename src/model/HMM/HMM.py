import pandas as pd
from collections import defaultdict

class HMM:
    def __init__(self) -> None:
        self.transition_matrix = defaultdict(defaultdict)
        self.counts_matrix = defaultdict(int)
    
    def get_transition_matrix(self):
        """
        Return the transition matrix
        """
        return self.transition_matrix

    def set_counts_matrix(self, X, y):
        """
        Return the counts matrix
        """
        counts_matrix = defaultdict(int)
        for train_exe in X:
            counts_matrix[train_exe] += 1
        for test_exe in y:
            counts_matrix[test_exe] += 1
        self.counts_matrix = counts_matrix
        return
    
    def get_counts_matrix(self):
        """
        Return the counts matrix
        """
        return self.counts_matrix

    def get_counts(self, exe):
        """
        Return the counts of the next executable occurance

        Parameters:
        exe (str): the name of the given executable name (prior)
        """
        match_ind = self.X[self.X == exe].index
        next_app = self.y.loc[match_ind]
        return next_app.value_counts()

    def fit(self, X, y):
        """
        Compute and return transition matrix

        Parameters:
        X (pd.Series): a series of given executable names
        y (pd.Series): a series of target executables names
        """
        self.X, self.y = X, y
        self.unique_exe = self.X.unique()
        self.n = len(self.unique_exe)
        self.dummy = pd.Series(data=[0.0] * self.n, index=self.unique_exe)
        self.set_counts_matrix(X, y)

        for exe in self.unique_exe:
            counts = self.get_counts(exe)
            prob = counts / counts.sum()
            prob_total = self.dummy.copy()
            prob_total[prob.index] = prob
            prob_total = prob_total.sort_values(ascending=False)
            self.transition_matrix[exe] = defaultdict(float, prob_total.to_dict())
        # return self.transition_matrix
    
    def predict(self, X_test, top=1):
        """
        Make prediction

        Parameters:
        X_test (pd.Series): test set
        top (int): Number of executables to predict for each datapoint

        Returns:
        Predictions of possible executables
        """
        y_pred = []
        for exe in X_test:
            next_exes = self.transition_matrix[exe]
            if len(next_exes) == 0:  # When the exe in test set does not appear in training set
                y_pred.append(['NaN'] * top)
            else:
                next_exe_pred = list(next_exes.keys())[:top]  # Get top X executables with highest transition probability
                y_pred.append(next_exe_pred)
        return y_pred

    def evaluate(self, y_pred, y_test):
        """
        Compute accuracy

        Parameters:
        y_pred (pd.Series): the ground truth
        y_test (pd.Series): the prediction from HMM model

        Return:
        Accuracy
        """
        count = 0
        for pred, target in zip(y_pred, y_test):
            if target in pred:
                count += 1
        return count / len(y_test)