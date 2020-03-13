#!/usr/bin/python

# Standard library imports
from collections import Counter

# Third party imports
import pandas as pd

# Local app imports


# -------------------------- EXTERNAL MODULES ABOVE -------------------------- #


def build_corpus(questions_df, answers_df):
    """docstring    """

    return {
        row.Id: {
            "title": row.Title,
            "body": row.Body,
            "answers": [
                answer.Body for _, answer
                in answers_df.loc[answers_df.ParentId == row.Id].iterrows()
            ]
        }
        for idx, row in questions_df.iterrows()
    }


def get_discussions_text(corpus, doc_id=False):
    """docstring"""

    if doc_id:
        corpus_text = {
            doc: " ".join([
                corpus[doc]["title"],
                corpus[doc]["body"],
                " ".join(corpus[doc]["answers"])
            ])
            for doc in corpus
        }
    else:
        corpus_text = [
            " ".join([
                corpus[doc]["title"],
                corpus[doc]["body"],
                " ".join(corpus[doc]["answers"])]
            )
            for doc in corpus
        ]

    return corpus_text


def corpus_word_frequency(corpus_text):
    """docstring"""

    bag_of_words = " ".join(corpus_text).split()
    frequency = Counter(bag_of_words)

    return pd.DataFrame.from_dict(
        data=frequency, orient='index', columns=['frequency'])
