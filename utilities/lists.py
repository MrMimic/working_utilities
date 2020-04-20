#!/usr/bin/env python3

from typing import Any, List, Union

import numpy as np


def flatten_list(list_of_list: List[List[Any]]) -> List[Any]:
    """
    Flatten list of lists into a single list.
    
    Args:
        list_of_list (List[List[Any]]): The list of list to be flatten.
    
    Returns:
        List[Any]: Flatten list.
    """    
    flat_list = [item for sublist in list_of_list for item in sublist]
    return flat_list


def remove_outliers(X: List[Union[int, float]], t: float = 3.5) -> List[Union[int, float]]:
    """
    Remove outliers from a numerical list X based on z-score > t.
    
    Args:
        X (List[Union[int, float]]): The list of numerical values to be filtered.
        t (float, optional): Threshold for the Z score. Defaults to 3.5.
    
    Returns:
        List[Union[int, float]]: List without outliers.
    """
    mean_X = np.mean(X)
    std_X = np.std(X)

    good_x = []

    for x in X:
        z_score = (x - mean_X) / std_X
        if z_score < t:
            good_x.append(x)
    return good_x


def split_into_chunks(iterable: List[Any], chunks_size: int = 1) -> List[List[Any]]:
    """
    Split an iterable into chunks of size chunks.
    Args:
        iterable (List[Any]): List to split.
        chunks_size (int, optional): Size of each chunk. Defaults to 1.
    Returns:
        List[Any]: List of batches.
    """
    batches = []
    total_size = len(iterable)
    for ndx in range(0, total_size, chunks_size):
        batches.append(iterable[ndx:min(ndx + chunks_size, total_size)])
    return batches
