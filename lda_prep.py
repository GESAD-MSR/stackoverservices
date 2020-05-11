# Standard library imports
import math
import pprint
import re
from collections import Counter

# Third party imports
import pandas as pd
import numpy as np
import dask.dataframe as dd

# Local app imports
from data_module.corpus import operations as op


# -------------------------- EXTERNAL MODULES ABOVE -------------------------- #


pp = pprint.PrettyPrinter(indent=4)

raw_questions = pd.read_csv('./questions_results/questions.csv')[["Id", "Title", "Body"]]
questions = raw_questions.replace(np.nan, '', regex=True)
raw_answers = pd.read_csv('./answers_results/answers.csv')[["Id", "ParentId", "Body"]]
answers = raw_answers.replace(np.nan, '', regex=True)

corpus = op.build_corpus(questions, answers)
corpus_text = op.get_discussions_text(corpus)
word_freq = op.corpus_word_frequency(corpus_text)
upper_range, lower_range = map(
 lambda corpus_limit: math.ceil(len(corpus_text) * corpus_limit), (0.8, 0.02))

lower_prune = word_freq.loc[word_freq.frequency < lower_range]
upper_prune = word_freq.loc[word_freq.frequency > upper_range]

prune_set = set(list(lower_prune.index) + list(upper_prune.index))
prune_corpus = op.get_discussions_text(corpus, doc_id=True)
prune_corpus_df = pd.DataFrame.from_dict(
    data=prune_corpus, orient='index', columns=['text'])
# print(prune_corpus_df.loc[prune_corpus_df.index == 47982972].text[47982972])

text = "\n\n".join(prune_corpus_df['text'])
count = 0

for word in prune_set:
    count += 1
    word = " " + word + " "  # this is done to ensure no substring matching
    text = re.sub(word, " ", text)
    if count % 1000 == 0:
        print(count)

prune_corpus_df['text'] = text.split(sep="\n\n")

lda_data = {
    "document": [],
    "word": [],
    "n": []
}


for idx, row in prune_corpus_df.iterrows():
    doc_text = prune_corpus_df.loc[prune_corpus_df.index == idx].text[idx]
    freq = Counter(doc_text.split())
    lda_data["document"] = lda_data["document"] + ([idx] * len(freq))
    lda_data["word"] = lda_data["word"] + list(freq.keys())
    lda_data["n"] = lda_data["n"] + list(freq.values())


lda_df = pd.DataFrame.from_dict(data=lda_data)
lda_df.to_csv('lda_input.csv', index=False)
