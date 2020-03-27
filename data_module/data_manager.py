import pandas as pd
# from .query_builder import QueryBuilder
from openpyxl import Workbook
# from google.cloud import bigquery


######################## Only eternal modules above ########################


def query_posts(query):
    """
    Query google's Big Query plataform

    Parameters
    ----------
    query : String
        SQL command for the specific database

    Returns
    -------
    Pandas.Dataframe
        DataFrame containing the rows resulted from the query

    See Also
    --------

    Examples
    --------

    """
    # client = bigquery.Client()
    # job = client.query(query)

    # result = job.result().to_dataframe()
    # result.set_index('Id', inplace=True)
    # result.fillna(0.0, inplace=True)

    # return result


def get_quantile_union(df, quantile, quantile_range='upper'):
    """
    Get part of the data above or below a determined quantile
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

    if quantile_range == 'upper':
        data = df.loc[
           (df.AnswerCount > q.AnswerCount) |
           (df.ViewCount > q.ViewCount) |
           (df.CommentCount > q.CommentCount) |
           (df.FavoriteCount > q.FavoriteCount) |
           (df.Score > q.Score)
        ]
    elif quantile_range == 'lower':
        data = df.loc[
            (df.AnswerCount < q.AnswerCount) |
            (df.ViewCount < q.ViewCount) |
            (df.CommentCount < q.CommentCount) |
            (df.FavoriteCount < q.FavoriteCount) |
            (df.Score < q.Score)
        ]
    else:
        print('Ivalid range of data')
        data = None

    return data, q


def get_quantile_intersections(df, quantile, quantile_range='upper'):
    """
    Get part of the data above or below a determined quantile
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

    if quantile_range == 'upper':
        data = df.loc[
            (df.AnswerCount > q.AnswerCount) &
            (df.ViewCount > q.ViewCount) &
            (df.CommentCount > q.CommentCount) &
            (df.FavoriteCount > q.FavoriteCount) &
            (df.Score > q.Score)
        ]
    elif quantile_range == 'lower':
        data = df.loc[
            (df.AnswerCount < q.AnswerCount) &
            (df.ViewCount < q.ViewCount) &
            (df.CommentCount < q.CommentCount) &
            (df.FavoriteCount < q.FavoriteCount) &
            (df.Score < q.Score)
        ]
    else:
        print('Ivalid range of data')
        data = None

    return data, q


def quantile_clustering(df, quantile_info):
    """docstring"""
    
    result = {}

    for index in quantile_info.index:
        filtered = df.loc[df[index] > quantile_info[index]]
        result[index] = list(filtered['Id'])
    
    return result
