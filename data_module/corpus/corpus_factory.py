#!/usr/bin/python

# Standard library imports
import re

# Third party imports
import pandas as pd

# Local app imports
from .lda_corpus import LDACorpus


# -------------------------- EXTERNAL MODULES ABOVE -------------------------- #


class CorpusFactory(object):
    """Docstring"""

    source_types = {"files", "data_frames"}

    def __init__(self, source):

        self.get_corpus = self.build_from_df
        self.get_corpus = self.build_from_files

    def get_corpus(self):
        """docstring"""
        raise Exception("method template, no behaviour defined")

    def build_from_df(self):
        """docstring"""
        pass

    def build_from_files(self):
        """docstring"""
        pass
