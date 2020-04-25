from scipy import stats
from typing import List


def check_normality(serie: List[float], alpha: int = 0.05) -> bool:
    """
    Performs a Shapiro and Wilk test on a serie of value to look for its normality.

    Args:
        serie (List[float]): A list of values.
        alpha (int, optional): The alpha to compare pvalue. Defaults to 0.05.

    Returns:
        bool: Wheter the serie is normal or not
    """
    stat, p = stats.shapiro(serie)
    print('Statistics=%.3f, p=%.3f' % (stat, p))

    if p > alpha:
        return True
    else:
        return False
