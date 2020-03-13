import os
import argparse
import pandas as pd
import logging

from data_module import data_manager as dm
from data_module.corpus import data_operations as do


######################## Only eternal modules above ########################

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


parser = argparse.ArgumentParser(
    description='Query and extract relevant data')

parser.add_argument(
    '-q', '--questions_query', metavar='Q', nargs=1,
    type=str, help='SQL file containing the query to SOTorrent questions')

parser.add_argument(
    '-a', '--answers_query', metavar='A', nargs=1,
    type=str, help='SQL file containing the query to SOTorrent answers')

args = vars(parser.parse_args())

# TODO: setup this data as a config json
DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/research_tool/')
ANSWERS_FILE = DATA_FOLDER + 'answers.csv'
QUESTIONS_FILE = DATA_FOLDER + 'questions.csv' 
UNION_FILE = DATA_FOLDER + 'relevance_union.csv'
INTERSECTION_FILE = DATA_FOLDER + 'relevance_intersection.csv'


if args['questions_query']:
    questions_query_path = args['questions_query'][0]
    
    with open(questions_query_path, 'r') as sql_file:
        questions_sql = sql_file.read()
    
    logger.info("Querying questions")
    questions = dm.query_posts(questions_sql)
    logger.info("Saving questions")
    questions.to_csv(QUESTIONS_FILE)
    logger.info(f"Questions saved at {QUESTIONS_FILE}")
else:
    logger.info("Questions query skipped\n")


if args['answers_query']:
    try:
        available_questions = pd.read_csv(QUESTIONS_FILE)
    except:
        raise Exception(
            "Questions not found. Check the questions file \
            or run a questions query")
    
    ids = list(available_questions["Id"])
    anwers_query_path = args['answers_query'][0]
    
    with open(anwers_query_path, 'r') as sql_file:
        answers_sql = sql_file.read()
    
    answers_sql = answers_sql + \
        f" WHERE ParentId IN ({', '.join([str(elem) for elem in ids])})" 
    
    answers = dm.query_posts(answers_sql)
    logger.info("SAVING ANSWERS")
    answers.to_csv(ANSWERS_FILE)
    logger.info(f"Answers saved at {ANSWERS_FILE}")
else:
    logger.info("Answers query skipped\n")
