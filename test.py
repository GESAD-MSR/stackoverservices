import pandas as pd
import numpy as np
import os
import glob
import pprint

from data_module import discussions as dcs
from data_module.corpus import clean
from data_module.corpus import operations as op


# pp = pprint.PrettyPrinter(indent=4)
# raw_quest = pd.read_csv('questions_test.csv')[["Id", "Title", "Body"]]
# quest = raw_quest.replace(np.nan, '', regex=True)
# raw_ans = pd.read_csv('answers_test.csv')[["Id", "ParentId", "Body"]]
# ans = raw_ans.replace(np.nan, '', regex=True)
#
# corpus = op.build_corpus(quest, ans)
#
# text_list = op.get_discussions_text(corpus)
# print(text_list[0])

# DATA_DIR =  os.path.join(os.path.dirname(__file__), 'data/mde/')
# def filter_many(docs_path):
#     questions_techs = glob.glob(docs_path+'raw/questions/*.csv')
#     answers_techs = glob.glob(docs_path+'raw/answers/*.csv')

#     for questions, answers in zip(sorted(questions_techs), sorted(answers_techs)):

#         tech_name = questions[questions.rfind('/')+1:questions.rfind('.')]

#         questions_df = pd.read_csv(questions)
#         print(len(questions_df.index))

#         answers_df = pd.read_csv(answers)

#         false_discussions = dcs.filter_no_discussions(questions_df, answers_df)

#         discussions = questions_df.loc[~questions_df.Id.isin(false_discussions)]
#         discussions.fillna(0.0, inplace=True)
#         discussions.set_index('Id', inplace=True)

#         print(len(discussions.index))

#         discussions.to_csv(
#             docs_path + 'filtered/discussions-' + tech_name + '.csv')


# filter_many(DATA_DIR)