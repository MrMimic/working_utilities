import numpy as np


class Lists(object):
    def __init__(self):
        pass

    def flatten_list(self, list_of_list):
        flat_list = [item for sublist in list_of_list for item in sublist]
        return flat_list

    def remove_outliers(self, X, Y, t=3.5):
        """ Remove outliers from a numerical list X based on z-score > t """

        mean_X = np.mean(X)
        std_X = np.std(X)

        good_x = []
        good_y = []

        for x, y in zip(X, Y):
            z_score = (x - mean_X) / std_X
            if z_score < t:
                good_x.append(x)
                good_y.append(y)
        return good_x, good_y
