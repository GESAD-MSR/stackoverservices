import pandas as pd
import os

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/current/raw/')

PREV_DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/previous/raw/')

ANSWERS_FILE = DATA_FOLDER + 'answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'questions.csv'

UNION_FILE = DATA_FOLDER + 'relevance_union.csv'
PREV_UNION_FILE = PREV_DATA_FOLDER + 'relevance_union.csv'

curr_file = pd.read_csv(UNION_FILE)
prev_file = pd.read_csv(PREV_UNION_FILE)


complement_data = curr_file.loc[~curr_file.Id.isin(prev_file.Id)]

intersection_data = curr_file.loc[curr_file.Id.isin(prev_file.Id)]
inter_intersection_data = prev_file.loc[
    ~prev_file.Id.isin(intersection_data.Id)]

# print(len(intersection_data.index))
print(inter_intersection_data.Id)

# curr_size = len(curr_file.index)
# prev_size = len(prev_file.index)
# data_diff = curr_size - prev_size

# print(f"size diff: {data_diff}")
# print(f"size complement: {len(complement_data.index)}")
