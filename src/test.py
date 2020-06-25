# from stackoverservices.data.corpus import filters

from typing import Tuple

import dask.dataframe as dd

from dask.dataframe.core import DataFrame, Series

import pandas as pd

import os

def filter_quantile_union(
    df: DataFrame,
    quantile: int,
    quantile_range: str = 'upper') -> Tuple[DataFrame, Series]:
    """
    Get part of the data above or below a determined quantile

     Parameters
    ----------
    df : DataFrame
        The dataframe from which the distribution should be estimated
    
    quantile : integer
        The distribution section to be used as threshold

    quantile_range : string
        default: upper
        The region which should be filtered, where upper indicates values
        above the quantile and lower otherwise

    Returns
    -------
    Two-Element Tuple
        A tuple where the first item is the resulting filtered dataframe
        and the second is a series with the quantile threshold value
    """

    if quantile == 1:
        q = df.quantile(q=0.25)
    elif quantile == 2:
        q = df.quantile(q=0.5)
    elif quantile == 3:
        q = df.quantile(q=0.75)
    else:
        print("Invalid quantile")
        return
    q = q.compute()
    q2 = q.to_frame()
    
    q2 = q2.transpose()
    q2 = q2.reset_index()

    if quantile_range == 'upper':
        data = df.loc[
            (df.AnswerCount > q2.AnswerCount) |
            (df.ViewCount > q2.ViewCount) |
            (df.CommentCount > q2.CommentCount) |
            (df.FavoriteCount > q2.FavoriteCount) |
            (df.Score > q2.Score)
        ]
    elif quantile_range == 'lower':
        data = df.loc[
            (df.AnswerCount < q2.AnswerCount) |
            (df.ViewCount < q2.ViewCount) |
            (df.CommentCount < q2.CommentCount) |
            (df.FavoriteCount < q2.FavoriteCount) |
            (df.Score < q2.Score)
        ]
    else:
        #TODO raise an error here
        print('Ivalid range of data')
        data = None

    return data, q

ddf = pd.read_csv('so_data_questions_1103')
dd = dd.from_pandas(ddf, npartitions= 3)

print(filter_quantile_union(dd, 1, 'upper'))