#!/usr/bin/python

# Standard library imports
import re

# Third party imports
import pandas as pd

# Local app imports


# -------------------------- EXTERNAL MODULES ABOVE -------------------------- #


class LDACorpus(object):
    """Docstring"""

    def __init__(self, corpus_dict):
        self.corpus = corpus_dict
        self.corpus_backup = None

    def build_corpus(self, questions_df, answers_df):
        """docstring"""
        pass

    def restore_corpus(self):
        """docstring"""
        pass

    def backup_corpus(self):
        """docstring"""
        pass

    def get_corpus_text(self):
        """docstring"""
        pass

    def get_pruned_corpus(self):
        """docstring"""
        pass

    def get_dtm(self):
        """docstring"""
        pass








