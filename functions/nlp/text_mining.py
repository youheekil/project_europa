#=============================================================#
#                    Necessary library                        #
#=============================================================#
import pandas as pd
import numpy as np 
import openpyxl
import nltk as nltk
import os
import sys 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize # passing string text into word tokenize for breaking the sentences
from string import punctuation


#=============================================================#
#                    Taxonomy data                            #
#=============================================================#
primary_path = "/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa/data"

path = ("/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa/data/external/sustainable-finance-teg-taxonomy-tools_en.xlsx")
# path = ("your path for file location - sustainable-finance-teg-taxonomy-tools_en.xlsx")

taxonomy = pd.read_excel(path, sheet_name='Mitigation summary', header=None)
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
taxonomy = taxonomy.drop([0, 1, 2])
taxonomy.to_excel(primary_path +  "/processed/taxonomy.xlsx", index = None)
#=============================================================#
#                    Matched data                            #
#=============================================================#
path2 = ("/Users/youheekil/Desktop/projects/modern_analytics /Final Project/final_project_eruopa/project_europa/data/processed/info_match_round2_CSPPholdings_201706_2021.csv")
match = pd.read_csv(path2)
description_test = match['Primary Industry description']
description_test.to_excel(primary_path + "/processed/test.xlsx", index = None)

x = description_test.shape[0] #nrows
for i in range(0,x):
    A = str(description_test[i])
    f = open(primary_path+"/processed/test.txt", "a")
    f.write(A+"\t")
    f.close()
    f = open(primary_path+"/processed/test.txt", "a")
    f.write("\n")
    f.close()
    

#=============================================================#
#                    Tokenize Text                            #
#=============================================================#

#sentences tokenized into
sustainable_contribution = str(list(taxonomy['Activity']))
sents = sent_tokenize(sustainable_contribution)
words = [word_tokenize(sent) for sent in sents] 

#import nltk
#nltk.download('stopwords')
customStopWords = set(stopwords.words('english')+list(punctuation))
wordsWOStopwords = [word for word in word_tokenize(sustainable_contribution) if word not in customStopWords]

from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordsWOStopwords)
sorted(finder.ngram_fd.items()) # distinct bigrams and their frequencies 



filepath = primary_path+"/processed/test.txt"
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        print("Column {}: {}".format(cnt, line.strip()))
        line = fp.readline()
        cnt += 1
        
with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        print("column {}:{}".format(cnt, line))











