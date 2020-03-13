#!/usr/bin/env python

import pandas as pd

from . import data_manager as dm
from .corpus import data_operations as do


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
    non_related.fillna(0.0, inplace=True)
    
    related = questions_df.loc[~questions_df.Id.isin(non_related_ids)]
    related.fillna(0.0, inplace=True)

    return related, non_related


def no_discussions_filter(questions_df, answers_df):
    """
    
    > Filter all questinos in wich the only the owner posted answers
    @return: list of questions ids which are not discussions 

    """

    not_dscs = []

    for idx, question in questions_df.iterrows():
        answers = answers_df.loc[answers_df.ParentId == question.Id]

        if len(answers.index) == 1:
            if answers.iloc[0].OwnerUserId == question.OwnerUserId:
                not_dscs.append(question.Id)
    
    valid_discussions = questions_df.loc[~questions_df.Id.isin(not_dscs)]
    valid_discussions.fillna(0.0, inplace=True)

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