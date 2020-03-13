import os
import argparse
import pandas as pd
import pprint

from data_module import data_filters as dtf
from data_module import data_manager as dm
from data_module.corpus import data_operations as do


pprinter = pprint.PrettyPrinter(width=140, indent=4)

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/current/raw/')

USR_ANSWERS_FILE = DATA_FOLDER + 'usr_answers.csv'
USR_QUESTIONS_FILE = DATA_FOLDER + 'usr_questions.csv'

ANSWERS_FILE = DATA_FOLDER + 'answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'questions.csv'
UNION_FILE = DATA_FOLDER + 'relevance_union.csv'

NON_RELATED = DATA_FOLDER + 'non_related.csv'

# TECH_SIMPLE_FILE = 'data/technologies_simple.csv'
# TECH_COMPOUND_FILE = 'data/technologies_compound.csv'

TECH_SIMPLE_FILE = DATA_FOLDER + 'tech_simple.csv'
TECH_COMPOUND_FILE = DATA_FOLDER + 'tech_compound.csv'

# Load discussions dataframes
questions_df = pd.read_csv(QUESTIONS_FILE)
answers_df = pd.read_csv(ANSWERS_FILE)

# Filter discussions in which the only answer was made by who asked the question
discussions = dtf.no_discussions_filter(questions_df, answers_df)

# Filter discussions using SatckOverflow metrics
relevant_data = dtf.relevance_filter(discussions, 3)

#filtering non related discussions
non_related_ids = pd.read_csv(NON_RELATED)['Id']
related, _ = dtf.non_related_filter(relevant_data, non_related_ids)


"""
Use this section to filter technical and non-technical discussions
from the most relevant discussions
"""

# Load Technologies data
tech_data = {
    "simple": pd.read_csv(TECH_SIMPLE_FILE)["tool"],
    "compound": pd.read_csv(TECH_COMPOUND_FILE)["tool"]
}

tech, nontech = dtf.tech_concpt_filter(related, answers_df, tech_data)

"""end section"""


"""
Uncomment the four line bellow to write results fo specific files,  
otherwise leave the comments to view the respctive data statistics
"""

# tech.set_index('Id', inplace=True)
# tech.to_csv(DATA_FOLDER + 'tech.csv')

# nontech.set_index('Id', inplace=True)
# nontech.to_csv(DATA_FOLDER + 'nontech.csv')

"""end section"""


reviewed = pd.read_csv(
    "./data/microservices/previous/nontech_discussions.csv")


review_candidates = nontech.loc[~nontech.Id.isin(reviewed.Id)]
review_candidates.set_index('Id', inplace=True)
review_candidates.to_csv(DATA_FOLDER + "review_candidates.csv")


"""
    Uncomment the code line bellow to see statistics, 
    otherwise leave the comments to write data to files
"""
# data, quantiles = dm.get_union(discussions, 3)

# quantiles = quantiles.drop('Id')

# # Getting Tech discussions metrics
# metric_filter = dm.quantile_clustering(tech_discussions, quantiles)

# print("\n\nTech dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     # Get number of metrics ocurrences
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(tech_discussions.index) * 100
    
#     pprinter.pprint((metric, brute_value, corpus_relevance))

#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))


# # Getting Non Tech discussions metrics
# metric_filter = dm.quantile_clustering(nontech_discussions, quantiles)

# print("\n\nNon Tech dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     # Get number of metrics ocurrences
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(nontech_discussions.index) * 100
    
#     pprinter.pprint((metric, brute_value, corpus_relevance))

#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))


# # Getting False Positive discussions metrics
# metric_filter = dm.quantile_clustering(false_positives, quantiles)

# print("\n\nInvalid dicussions metrics\n\n")

# print("Metric\t\tTotal\t\tPercentual")
# for metric in metric_filter:
#     brute_value = len(metric_filter[metric])
#     corpus_relevance = brute_value / len(nontech_discussions.index) * 100
    
#     # print( "%s\t\t\t%d\t\t\t%f" % (metric, brute_value, corpus_relevance))
#     pprinter.pprint((metric, brute_value, corpus_relevance))


# print(len(nontech_discussions.index))
# print(len(tech_discussions.index))

"""end section"""