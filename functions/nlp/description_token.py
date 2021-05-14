# description_token.py
import pandas as pd
import os
path = ('/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa')

import numpy as np 
import openpyxl

#sentencize
import re
import spacy

#tokenize (!pip install nltk)
import nltk
nltk.download('punkt')


# sentencizer pipeline component
from spacy.lang.en import English

# tokenize an first_description text using nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# read the file
df = pd.read_csv(path + "/data/processed/info_match_round2_CSPPholdings_201706_2021.csv")

# tokenize the sentences 
nlp = spacy.load("en_core_web_sm")
df['Primary Industry description'] = df['Primary Industry description'].apply(lambda x: [sent.text for sent in nlp(x).sents])
df = df.explode("Primary Industry description", ignore_index=True)
df.rename(columns={"Name_1": "Company Name"}, inplace=True)
df.index.name = "Sentence ID"
df.to_csv("description_tokenized.csv")

# tokenize the words
from nltk.tokenize import TreebankWordTokenizer

## initialize treenbankword tokenizer 
tokenizer = TreebankWordTokenizer()

df['words'] = df['Primary Industry description'].apply(lambda x: [words for words in tokenizer.tokenize(x)])

# Stemming and lemmatization 
#nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

## initialize lemmatizer
lemmatizer = WordNetLemmatizer()

## initialize stemmer
stemmer = SnowballStemmer("english")
words = df.loc[1, 'words']


    
    