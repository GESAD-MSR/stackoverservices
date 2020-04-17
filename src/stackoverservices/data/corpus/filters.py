#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module presents a series of functions to filter dataframes.

"""


# ============================== IMPORT SECTION ============================== #


# Standart libs
#
from typing import Tuple

# External libs
#
from pandas import DataFrame, Series

# Local libs
#

__author__ = "Alan Bandeira"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Alan Bandeira"
__email__ = "alan.p.bandeira@gmail.com"
__status__ = "Development"


# =============================== CODE SECTION =============================== #


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
        #TODO raise an error here
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


def filter_by_words(questions_df, answers_df, simple_words, compound_words):
    """ docstring """

    matched_ids = []
    not_matched_ids = []

    simple_word_set = set(simple_words)

    punctuation_rgx = r"[^()[\]<>+\-_=\*|\^{}$&%#@!?.,:;/\"]+"

    for index, row in questions_df.iterrows():

        found_flag = False

        title = row.Title.lower()

        in_title_compound = [
            True if re.compile(compound_word).search(title) else False 
            for compound_word in compound_words]
        
        clean_text = re.findall(punctuation_rgx, title)
        clean_text = [word for line in clean_text for word in line.split()]
        clean_text = list(map(clean.remove_single_quotes, clean_text))
        
        simple_matched = simple_word_set.intersection(set(clean_text))
        in_title_simple = [True] * len(simple_matched)
        in_title = in_title_compound + in_title_simple

        if any(in_title):
            found_flag = True
        else:
            body = row.Body.lower()

            in_body_compound = [
                True if re.compile(compound_word).search(body) else False 
                    for compound_word in compound_words]
            
            clean_text = re.findall(punctuation_rgx, body)
            clean_text = [word for line in clean_text for word in line.split()]
            clean_text = list(map(clean.remove_single_quotes, clean_text))

            simple_matched = simple_word_set.intersection(set(clean_text))
            in_body_simple = [True] * len(simple_matched)
            in_body = in_body_compound + in_body_simple

            if any(in_body):
                found_flag = True
            else:
                answers = answers_df.loc[answers_df.ParentId == row.Id]

                for idx, line in answers.iterrows():
                    
                    answer = line.Body.lower()

                    in_answers_compound = [
                        True if re.compile(compound_word).search(answer) else
                        False for compound_word in compound_words]
                    
                    clean_text = re.findall(punctuation_rgx, answer)
                    clean_text = [
                        word for line in clean_text for word in line.split()]
                    
                    clean_text = list(
                        map(clean.remove_single_quotes, clean_text))

                    simple_matched = simple_word_set.intersection(
                        set(clean_text))
                    in_answers_simple = [True] * len(simple_matched)
                    in_answers = in_answers_compound + in_answers_simple

                    if any(in_answers):
                        found_flag = True
                        break
        
        if found_flag:
            matched_ids.append(row.Id)
        else:
            not_matched_ids.append(row.Id)
        
    return matched_ids, not_matched_ids


def relevance_filter(questions_df, quantile, output=None, metric="union"):
    """
    
    Filter a questions dataframe using stackoverflow metrics based on boxplot 
    quartiles.

    :param questions_df
        > A pandas dataframe of stackoverflow questions containing 
        posts' relevance metrics;

    :param quartile
        > Integer indicating distribution thershold;
    
    :param output
        > File path to write results, default value is None;

    :param metric
        > Data selecting metric, following the available methods inside
        data_manager package. Currently union and intersection are available.
            
    :return (tuple):
        > Dataframe of relevant discussions;
    
    """

    if metric is "union":
        relevant, q = dm.get_quantile_union(questions_df, quantile)
    else:
        relevant, q = dm.get_quantile_intersections(questions_df, quantile)
    
    if output:
        to_persist = relevant.set_index('Id')
        to_persist.to_csv(output)

    return relevant


def non_related_filter(questions_df, non_related_ids):
    """
    
    Splits a questions dataframe between related and non-related discussions, 
    based on an Ids list of non-related discussions.

    :param questions_df:
        > A pandas dataframe of stackoverflow questions containing posts Ids;

    :param non_related_ids:
        > List like object containing Ids of manually filtered non-related 
        stack overflow discussions;
            
    :return (tuple):
        > Two dataframes, one with related discussions and another with 
        non-related discussions
    
    """

    non_related = questions_df.loc[questions_df.Id.isin(non_related_ids)]
    non_related = non_related.fillna(0.0)
    
    related = questions_df.loc[~questions_df.Id.isin(non_related_ids)]
    related = related.fillna(0.0)

    return related, non_related


def no_discussions_filter(questions_df, answers_df):
    """
    
    > Filter all questions in wich the only the owner posted answers
    @return: list of questions ids which are not discussions 

    """

    not_dscs = []

    for idx, question in questions_df.iterrows():
        answers = answers_df.loc[answers_df.ParentId == question.Id]
        print(idx)
        if len(answers.index) == 1:
            if answers.iloc[0].OwnerUserId == question.OwnerUserId:
                not_dscs.append(question.Id)
    
    valid_discussions = questions_df.loc[~questions_df.Id.isin(not_dscs)]
    valid_discussions = valid_discussions.fillna(0.0)

    return valid_discussions


def tech_concpt_filter(questions_df, answers_df, tehcs_dict):
    """docstring"""
    
    # Transform tech lists text itens to lower case to assure consistency
    simple_tech = list(map(lambda x: x.lower(), tehcs_dict["simple"]))
    compound_tech = list(map(lambda x: x.lower(), tehcs_dict["compound"]))

    # Word filtering
    tech_ids, nontech_ids = do.filter_by_words(
        questions_df, answers_df, simple_tech, compound_tech)

    tech_discussions = questions_df.loc[questions_df.Id.isin(tech_ids)]
    nontech_discussions = questions_df.loc[questions_df.Id.isin(nontech_ids)]

    return tech_discussions, nontech_discussions