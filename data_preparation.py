# Standard library imports
import os
from sys import exit
from functools import partial

# Third party imports
import spacy
import pandas as pd
from bs4 import BeautifulSoup
import dask.dataframe as dd

# Local app imports
from data_module.corpus import clean

# -------------------------- EXECUTION STARTS BELLOW ------------------------- #

nlp = spacy.load('en_core_web_sm')

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/microservices/research_tool/')

questions = dd.read_csv(DATA_FOLDER + 'datasetLDAAlan.csv', dtype={'OwnerUserId': 'float64'})
questions = questions.fillna(0.0)

# answers = dd.read_csv(DATA_FOLDER + 'answers.csv')
# answers = answers.fillna(0.0)

my_stop_words = set(open('misc/stopword_list.txt', 'r').read().split("\n"))

# QUESTIONS CLEANING STAGE
print("STARTING QUESTIONS\n\n")

# Cleaning questions title
print("Starting Title")
print("Cleaning data start")

questions.Title = questions.Title.map_partitions(clean.plus_ultra, my_stop_words, nlp)

print("Title complete")

# Cleaning questions text from HTML

print("\n\nStarting questions Body")
print("Cleaning data start")

questions.Body = questions.Body.map_partitions(clean.go_beyond)
questions.Body = questions.Body.map_partitions(clean.plus_ultra, my_stop_words, nlp)

questions.to_csv('questions_results/*.csv', index=False)
print("QUESTIONS FINISHED\n\n")

# # ANSWERS CLEANING STAGE
# print("STARTING ANSWERS\n\n")
# print("Starting answers Body")

# print("Cleaning data start")

# answers.Body = answers.Body.map_partitions(clean.go_beyond)
# answers.Body = answers.Body.map_partitions(clean.plus_ultra, my_stop_words, nlp)

# print("Answers complete")

# answers.to_csv('answers_results/*.csv', index=False)
# print("ANSWERS FINISHED\n\n")
