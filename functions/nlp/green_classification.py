# green_classification.py
import pandas as pd
import os
path = '/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa/'
os.chdir(path)

import numpy as np 
import openpyxl

#sentencize
import re
import spacy

# ==================================================================== #
#                    Stemming and lemmatization                        #
# ==================================================================== #
sents = sent_tokenize(sustainable_contribution)
words = [word_tokenize(sent) for sent in sents] 

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# initialize stemmer
stemmer = SnowballStemmer("english")

# sents = sent_tokenize(sustainable_contribution)
df['sent'] = [sent_tokenize(df_sents) for df_sents in df['Primary Industry description']]
df['words'] = [word_tokenize() for d_words in df['sent']]

   

    
# ==================================================================== #
#                       text cleaning                                  #
# ==================================================================== #
import re
import string
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
# passing string text into word tokenize for breaking the sentences
from nltk.tokenize import word_tokenize, sent_tokenize 
from string import punctuation

def clean_text(s):
    """
    This function cleans the text a bit
    @param s: string 
    return: cleaned string 
    """
    # split by all whitespaces
    s = s.split()
    
    # join tokens by single space
    # this will allow us to remove all kinds of weird space
    s = " ".join(s)
    s = s.lower()
    
    # remove all punctuations using regex and string module 
    s = re.sub(f'[{re.escape(string.punctuation)}]', '', s)
    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    s = pattern.sub('', s)    
    # return the cleaned string 
    return s


corpus_taxonomy = pd.read_excel(path + "/data/processed/taxonomy.xlsx")
corpus_taxonomy.loc[:, "Activity"] = corpus_taxonomy.Activity.apply(clean_text)

corpus_tok_description = pd.read_csv(path + "/data/processed/description_tokenized.csv")
corpus_tok_description.loc[:, "Primary Industry description"] = corpus_tok_description["Primary Industry description"].apply(clean_text)

# ==================================================================== #
#                  NMF - non-negative matrix factorization             #
#                       latent semantic analysis(LSA)                  #
# ==================================================================== #
# which is popularly known as singular value decomposition or SVD. 
# CountVectorizer or TfidfVectorizer

# get the topic from the taxonomy data

import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn import decomposition
from sklearn.feature_extraction.text import TfidfVectorizer
import sys


# create a corpus of sentences # @corpus ??
# we read samples from training data
# for this data

#corpus =  pd.read_excel(path + "/data/processed/taxonomy.xlsx")
corpus = corpus_taxonomy
corpus = corpus['Activity'].values

# initialize TfidfVecorizer with word_toeknize from nltk as the tokenizer
tfv = TfidfVectorizer(tokenizer = word_tokenize, token_pattern = None)

# fit the vectorizer on corpus
tfv.fit(corpus)

#transform the corpus using tfidf 
corpus_transformed = tfv.transform(corpus)

# initialize SVD with 10 components 
svd = decomposition.TruncatedSVD(n_components = 10)

# fit SVD
corpus_svd = svd.fit(corpus_transformed)

# choose first sample and create a dictionary
# or feature names and their scores from svd
# you can change the sample_index variable to 
# to get dictionary for any other sample 
sample_index = 0 
feature_scores = dict(
    zip(
        tfv.get_feature_names(), 
        corpus_svd.components_[sample_index]
    )
)

# once we have the dictionary, we can now
# sort it in decreasing order and get the 
# top N topics
N = 10
# make sure the directory is set as "/data/processed"
#os.chdir(path + "/data/processed")

# save result as txt file titled green_classification. 
#sys.stdout = open("green_classification.txt", "w")
classification = []

for sample_index in range(N):
    feature_scores = dict(
        zip(
            tfv.get_feature_names(), 
            corpus_svd.components_[sample_index]
        )
    )
    result = sorted(
            feature_scores, 
            key = feature_scores.get, 
            reverse = True
            )[:N]
    classification.append(result)
    print(result)

#saved_stdout = sys.stdout 
#sys.stdout.close()
#sys.stdout = saved_stdout

# create a dictionary of green_classification
green_classification = dict(list(enumerate(classification)))
for key in green_classification:
    print('class:', key, 'has words of ', green_classification[key])
# ==================================================================== #
#                       detect green-                                  #
# ==================================================================== #
import itertools


# green
green = list(itertools.chain(*classification))

# data 
df = pd.read_csv(path + "/data/processed/description_tokenized.csv")
# clean the data 
df.loc[:, "Primary Industry description"] = df["Primary Industry description"].apply(clean_text)
 
# for loop to assign how many 'green' words are included. 
for label, row in df.iterrows():
    sentence = df.loc[label, 'Primary Industry description']
    # split sentence by a space
    # make sentence into a set
    sentence = set(sentence.split(" "))
    # check number of common words with green 
    df.loc[label, 'green'] = int(len(sentence.intersection(green)))
    if df.loc[label, 'green'] >= 1 :
        df.loc[label, 'sustainable_contribution'] = True
        df.loc[label, 'green_word'] = sentence.intersection(green) # store matching words
    else: 
        df.loc[label, 'sustainable_contribution'] = False
        df.loc[label, 'green_word'] = 0
    
        

         
# add number of the green words in the description -> what's green company and not green company
# based on the result, we probably can use the bert model for prediction later -> create the model
 
