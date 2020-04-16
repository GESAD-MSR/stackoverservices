#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module presents a series of functions to convert raw data.

"""


# ============================== IMPORT SECTION ============================== #


# Standart libs
#
import re
import string
from functools import partial
from collections import Set

# External libs
#
import pandas as pd

from spacy.lang.en import English
from bs4 import BeautifulSoup

# Local libs
#

__author__ = "Alan Bandeira"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Alan Bandeira"
__email__ = "alan.p.bandeira@gmail.com"
__status__ = "Develpment"


# =============================== CODE SECTION =============================== #


def lemmatization(nlp: English, text: str) -> str:
    """Extract words' lemma from a specific text using Spacy as NLP engine

    Parameters
    ----------
    nlp : English
        An instance of spacy english language model en_core_web_sm,
        created as follows.
            'nlp = spacy.load('en_core_web_sm')'
    
    text : string
        The text that should be lemmatized

    Returns
    -------
    string
        A text analogous to the input text, where each word is 
        switched for it's lemma.
    """

    processed_text = nlp(text)
    
    lemmatized_text = " ".join(
        [word.lemma_ for word in processed_text
         if word.lemma_ != "-PRON-" and word.lemma_ != "'s"]
    )

    return lemmatized_text


def remove_stopwords(stop_words: Set, text: str) -> str:
    """Remove the occurrence of all stop words provided in the set

    Parameters
    ----------
    stop_words : Set
        The set of words that should be removed
    
    text : string
        The text in which from the stop_words will be removed

    Returns
    -------
    string
        A text analogous to the input text, not including stopwords
    """
    
    text = text.split()
    words_to_remove = stop_words.intersection(set(text))
    cleaned_list = [word for word in text if word not in words_to_remove]
    return " ".join(cleaned_list)


def remove_quotation_marks(text: str) -> str:
    """Remove single quotation marks

    Parameters
    ----------
    text : string 
        The string containing a word surrounded by single quotation marks

    Returns
    -------
    string
        A word without single quotation marks
    """

    return " ".join(
        re.sub(r"[\'´`’\"]+", " ", text.lower()).split())


def remove_punctuation(text):
    """Remove the punctuation characters from a given text,
    based on a regular expression

    Parameters
    ----------
    text : string
        The string containing raw textual data

    Returns
    -------
    string
        A text analogous to the input text, without punctuation
    """

    return " ".join(
        [token for token in text.split() if token not in string.punctuation])


def remove_numeric_digits(text: str) -> str:
    """Remove numeric characters using regex
    
    Parameters
    ----------
    text : string
        A string containing numeric digits

    Returns
    -------
    string
        A string analogous to the input, but without numeric digits,
        removed using regex
    """
    clean_text = re.sub(r'[0-9]+', " ", text.lower())
    return " ".join(clean_text.split())


def remove_special_characters(text: str) -> str:
    """
    Remove specific characters related to digital written language using regex
    
    Parameters
    ----------
    text : string
        The raw text data containing special characters

    Returns
    -------
    string
        A string analogous to the input, but without special characters such as
        @, #, or underscores

    """

    special_rgx = r'[()[\]<>+\-_ = ~´`’\*|\^{}$&%#@!?.,:;/\"\\]+'
    clean_text = re.sub(special_rgx, " ", text.lower())
    return " ".join(clean_text.split())


def html_extraction(text: str) -> str:
    """
    Remove from the text html tags found on stack overflow data.

    Parameters
    ----------
    text : string
        The textual raw data containing specific html tags found on
        stack overflow dataset

    Returns
    -------
    string
        A string analogous to the input, in which specific
        html tags and it's content are removed, while other
        tags are remove but maintain their content

    """

    soup = BeautifulSoup(text, 'lxml')
    tags = ('a', 'div', 'code', 'blockquote')

    for tag in tags:
        for occurrence in soup.find_all(tag):
            _ = occurrence.extract()

    return " ".join(soup.text.split())

#TODO

def plus_ultra (df, my_stop_words, nlp):
    stop_words_remover = partial(remove_stopwords, my_stop_words)

    lemmatizator = partial(lemmatization, nlp)

    df = list(map(remove_numeric_digits, df))
        
    df = list(map(remove_special_characters, df))

    # print("lemmatization start")
    df = list(map(lemmatizator, df))

    # print("removing punctuation")
    df = list(map(remove_punctuation, df))

    # print("removing quotation marks")
    df = list(map(remove_quotation_marks, df))

    # print("removing stop_words")
    df = list(map(stop_words_remover, df))
    return df