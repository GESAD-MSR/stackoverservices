# Standard library imports
import re
import os

# Third party imports
import pandas as pd

# Local app imports
from data_module.corpus import clean


########################### EXECUTION STARTS BELLOW ############################


DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/research_tool')

raw_questions = pd.read_csv(DATA_FOLDER + 'questions.csv')
raw_answers = pd.read_csv(DATA_FOLDER + 'answers.csv')


# TODO add images information
# TODO add interaction information
# TODO add discussion information
# TODO extract links
# TODO extract code information
