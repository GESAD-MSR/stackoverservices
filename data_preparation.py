# Standard library imports
import os
# from sys import exit
from functools import partial

# Third party imports
import spacy
import pandas as pd
from bs4 import BeautifulSoup
import dask.dataframe as dd
import csv

# Local app imports
from data_module.corpus import clean
from data_module import data_filters
from data_module.corpus import data_operations

# -------------------------- EXECUTION STARTS BELLOW ------------------------- #

nlp = spacy.load('en_core_web_sm')

DATA_FOLDER = os.path.join(
    os.path.dirname(__file__), 'data/')

questions = dd.read_csv(DATA_FOLDER + 'so_data_questions_1103', dtype={'OwnerUserId': 'float64'})
questions = questions.fillna(0.0)

answers = dd.read_csv(DATA_FOLDER + 'so_data_answers_1103')
answers = answers.fillna(0.0)

my_stop_words = set(open('misc/stopword_list.txt', 'r').read().split("\n"))

# stop_words_remover = partial(clean.remove_stopwords, my_stop_words)

# lemmatizator = partial(clean.lemmatization, nlp)

# QUESTIONS CLEANING STAGE

print("STARTING QUESTIONS\n\n")

print('Cleaning No-Discussion Questions')

questions = data_filters.no_discussions_filter(questions,answers)

print('Filtering Complete')

# Cleaning questions title
print("Starting Title")
print("Cleaning data start")

# questions['Title'] = list(questions.Title.map_partitions(clean.remove_numeric_digits))
# questions['Title'] = list(questions.Title.map_partitions(clean.remove_special_characters))

# print("lemmatization start")
# questions['Title'] = list(questions.Title.map_partitions(lemmatizator))

# print("removing punctuation")
# questions['Title'] = list(questions.Title.map_partitions(clean.remove_punctuation, questions['Title']))
# print("removing quotation marks")
# questions['Title'] = list(map(clean.remove_quotation_marks, questions['Title']))
# print("removing stop_words")
# questions['Title'] = list(map(stop_words_remover, questions['Title']))

questions.Title = questions.Title.map_partitions(clean.plus_ultra, my_stop_words, nlp)

print("Title complete")

# Cleaning questions text from HTML

print("\n\nStarting questions Body")
print("Cleaning data start")

questions.Body = questions.Body.map_partitions(clean.go_beyond)
questions.Body = questions.Body.map_partitions(clean.plus_ultra, my_stop_words, nlp)

questions.to_csv('questions_results/questions.csv', index=False, single_file=True)
print("QUESTIONS FINISHED\n\n")

# ANSWERS CLEANING STAGE
print("STARTING ANSWERS\n\n")
print("Starting answers Body")

print("Cleaning data start")

answers.Body = answers.Body.map_partitions(clean.go_beyond)
answers.Body = answers.Body.map_partitions(clean.plus_ultra, my_stop_words, nlp)

print("Answers complete")

answers.to_csv('answers_results/answers.csv', index=False, single_file=True)
print("ANSWERS FINISHED\n\n")
