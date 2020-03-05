from scipy.stats import shapiro


class Stats(object):
    """
    Stats utilities
    """

    def __init__(self):
        pass

    def check_normality(self, serie, alpha=0.05):
        """
        Performs a Shapiro and Wilk test on a serie of value to look for its normality

        :param serie: A list of values
        :type serie: list
        :param alpha: The alpha to compare pvalue
        :type alpha: float
        :returns: Wheter the serie is normal or not
        :rtype: bool
        """

        stat, p = shapiro(serie)
        print('Statistics=%.3f, p=%.3f' % (stat, p))

        if p > alpha:
            return True
        else:
            return False
