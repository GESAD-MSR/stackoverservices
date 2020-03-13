import pandas as pd

# TODO DEPRECATED
# def filter_no_discussions(questions_df, answers_df):
#     """
    
#     > Filter all questinos in wich the only the owner posted answers
#     @return: list of questions ids which are not discussions 

#     """

#     not_dscs = []

#     for idx, question in questions_df.iterrows():
#         answers = answers_df.loc[answers_df.ParentId == question.Id]

#         if len(answers.index) == 1:
#             if answers.iloc[0].OwnerUserId == question.OwnerUserId:
#                 not_dscs.append(question.Id)

#     return not_dscs

