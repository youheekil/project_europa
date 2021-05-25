# description_token.py
import pandas as pd
import os
import sys 
import numpy as np 
import openpyxl

#sentencize
import re
import spacy
import string

#tokenize (!pip install nltk)
import nltk
#nltk.download('punkt')


# sentencizer pipeline component
from spacy.lang.en import English

# tokenize description text using nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# text cleaning 
import string
##nltk.download('stopwords')
from nltk.corpus import stopwords
##passing string text into word tokenize for breaking the sentences
from nltk.tokenize import word_tokenize, sent_tokenize 
from string import punctuation
from sklearn import model_selection
import torch


# topic extraction 
from sklearn import decomposition
from sklearn.feature_extraction.text import TfidfVectorizer

# detect green company by matching words
import itertools
from itertools import chain
from ast import literal_eval
#=============================================================#
#                            data                             #
#=============================================================#
def data_import(path):
    """
    this function is importing taxonomy daata and
    df
    """
    # read taxonomy data
    taxonomy = pd.read_excel(path + "/data/external/sustainable-finance-teg-taxonomy-tools_en.xlsx", sheet_name='Mitigation summary', header=None) 
    # rename taxonomy data columns 
    taxonomy.columns = [
    "NACE Macro-sector", 
    "Activity", 
    "Climate change mitigation_TYC",#Type of Contribution
    "Climate change mitigation_OP", #Own performance 
    "Climate change mitigation_En", #Enabling 
    "Climate change mitigation_TA", #Transition activity
    "Climate change adaptation_TYC", #Type of Contribution
    "Water_TYC", 
    "Circular economy_TYC", 
    "Pollution_TYC", 
    "Ecosystems_TYC"
]
    # drop unnecessary columns
    taxonomy = taxonomy.drop([0, 1, 2])
    # save the new excel file
    taxonomy.to_excel(path +"/data/processed/taxonomy.xlsx", index = None)
    # Match data which is our primary dataset to use for NLP
    df = pd.read_csv(path + "/data/processed/5_info_match_round2_CSPPholdings_201706_2021.csv")
    df.to_csv(path +"/data/processed/match_df.csv", index = None)
    return taxonomy, df


# path 
path = ("/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa")

# run the data import function 
data_import(path)

# read datafile 
taxonomy = pd.read_excel(path + "/data/processed/taxonomy.xlsx")
df = pd.read_csv(path + "/data/processed/match_df.csv")

# ==================================================================== #
#                       text cleaning                                  #
# ==================================================================== #

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
    
# cleaning taxonomy activity dataset 
taxonomy.loc[:, "Activity"] = taxonomy.Activity.apply(clean_text)
# cleaning match dataset
df.loc[:, "Primary Industry description"] = df["Primary Industry description"].apply(clean_text)


#=============================================================#
#                                Tokenize                     #
#=============================================================#

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

# remove any stopwords 
customStopWords = set(stopwords.words('english')+list(punctuation))
df['words'] = df['words'].apply(lambda x: [word for word in x if word not in customStopWords])

# ==================================================================== #
#                    Stemming and lemmatization                        #
# ==================================================================== #
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# initialize stemmer
stemmer = SnowballStemmer("english")

# ==================================================================== #
#                               Topic Extraction                       #
# ==================================================================== #
# create a corpus of sentences # @corpus ??
corpus = taxonomy['Activity'].values

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
    

#saved_stdout = sys.stdout 
#sys.stdout.close()
#sys.stdout = saved_stdout

# create a dictionary of green_classification
green_classification = dict(list(enumerate(classification)))
for key in green_classification:
    print('\nTopic', key, ':', green_classification[key])

# ==================================================================== #
#            detect green company by matching words                    #
# ==================================================================== #
# green
green_list = list(itertools.chain(*classification))
green = []
for greens in green_list:
        g_lemma = lemmatizer.lemmatize(greens)
        green.append(g_lemma)

print(f"\n\nSustainable Contribution Activities are consisted of {green}.")   

#df.loc[:, "Primary Industry description"] = df["Primary Industry description"].apply(clean_text)
 
# for loop to assign how many 'green' words are included. 
for label, row in df.iterrows():
    sentence = df.loc[label, 'Primary Industry description']
    # split sentence by a space
    # make sentence into a set
    sentence = set(sentence.split(" "))
    words = []
    # decided to just only apply lemmatizer
    # apply lemma as lemmatizer.lemmatize(word)
    for word in sentence:
        lemma = lemmatizer.lemmatize(word)
        words.append(lemma)   
    words = set(words) 
    # check number of common words with green 
    df.loc[label, 'green'] = int(len(words.intersection(green)))
    if df.loc[label, 'green'] >= 1 :
        df.loc[label, 'sustainable_contribution'] = True
        df.loc[label, 'green_word'] = str(list(words.intersection(green)))
    else: 
        df.loc[label, 'sustainable_contribution'] = False
        df.loc[label, 'green_word'] = 'None'

df.loc[:,'green_word'] = df.loc[:, 'green_word'].apply(lambda x: literal_eval(x))

# ==================================================================== #
#                          Extract Green Company                       #
# ==================================================================== #

green_company= df[df['sustainable_contribution'] == True] 
green_company.to_csv("green_company.csv")

gcp = green_company['Company Name'].unique()

# number of matched green company by the 10 topics 
print(f"\n\nThe number of detected green company is {gcp.shape[0]} \n\n The detected companies are {gcp}")
# todo: :complete: add number of the green words in the description 
# todo: :further: based on the result, we probably can use the bert model for prediction later -> create the model


