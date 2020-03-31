#!/usr/bin/python

# Standard library imports
import re
import string
from functools import partial

# Third party imports
import pandas as pd
from bs4 import BeautifulSoup

# Local app imports


# -------------------------- EXTERNAL MODULES ABOVE -------------------------- #


def lemmatization(nlp, text):
    """Extract words' lemma from a specific text using Spacy as NLP engine

    Parameters
    ----------
    nlp : Spacy
        The core instance of spacy usually defined as:
        'nlp = spacy.load('en_core_web_sm')'
    
    text : string
        The text that should be lemmatized

    Returns
    -------
    str
        a string of lemmas extracted from previous words in the text
    """

    processed_text = nlp(text)
    lemmatized_text = " ".join(
        [word.lemma_ for word in processed_text
         if word.lemma_ != "-PRON-" and word.lemma_ != "'s"]
    )

    return lemmatized_text


def remove_stopwords(stop_words, text):
    """Remove the occurrence of all stop_words provided in the list

    Parameters
    ----------
    stop_words : set
        The set of words that should be removed
    
    text : str
        The text in which from the stop_words will be removed

    Returns
    -------
    str
        a string representing the text without stopwords
    """
    
    text = text.split()
    words_to_remove = stop_words.intersection(set(text))
    cleaned_list = [word for word in text if word not in words_to_remove]
    return " ".join(cleaned_list)


def remove_quotation_marks(text):
    """Remove single quotation marks

    Parameters
    ----------
    text : str
        The string containing a complete word

    Returns
    -------
    str
        a word without single quote marks
    """

    return " ".join(re.sub(r"[\'´`’\"]+", " ", text.lower()).split())


def remove_punctuation(text):
    """Remove the punctuation and numerical characters from a given text,
    based on a regular expression

    Parameters
    ----------
    text : str
        The string containing textual data

    Returns
    -------
    str
        a string of words without punctuation
    """

    return " ".join(
        [token for token in text.split() if token not in string.punctuation])


def remove_numeric_digits(text):
    """
    Remove numeric digits using regex
    :param text:
    :return: text without numeric digits
    """
    textParam = text
    digits_rgx = r'[0-9]+'
    clean_text = re.sub(digits_rgx, " ", text.lower())
    return " ".join(clean_text.split())


def remove_special_characters(text):
    """
    Remove specific characters related to digital spoken language using regex
    :param text:
    :return: text without special characters
    """

    # special_rgx = r'[_.|\-:;/(){}[\]]+'
    special_rgx = r'[()[\]<>+\-_ = ~´`’\*|\^{}$&%#@!?.,:;/\"\\]+'
    clean_text = re.sub(special_rgx, " ", text.lower())
    return " ".join(clean_text.split())


def html_extraction(text):
    """
    Remove from the text html tags found on stack overflow data.

    :param text: string containing textual data mixed with specific html tags
    found on stack overflow data
    :return: a string in which specific html tags and it's content are removed
    and others tags are remove but not their content
    """

    soup = BeautifulSoup(text, 'lxml')
    tags = ('a', 'div', 'code', 'blockquote')

    for tag in tags:
        for occurrence in soup.find_all(tag):
            _ = occurrence.extract()

    return " ".join(soup.text.split())

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

def go_beyond(df):

    df = list(map(html_extraction, df))

    return df