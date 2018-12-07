import re
import sys
sys.path.append("../..")
import nltk
import string
import os
import os.path
import collections
import pickle
import features
import training

from features import *
from collections import Iterable
from nltk.corpus import conll2000
from nltk.chunk import conlltags2tree,tree2conlltags,ChunkParserI
from nltk.tag import ClassifierBasedTagger
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline


import project_config.py as config
from libs.models.File import File
from libs.models.RawFile import RawFile

from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from libs.nlp_engine.VoteClassifier import VoteClassifier




#array [ 'IOB','IOB'] to (word , pos-tag ,IOB)
def to_standard_form(tokens,pos_tag,iob):
    standard_form = []
    for i in range(len(tokens)):
        standard_form.append((tokens[i],pos_tag[i][1],iob[i]))
    return standard_form



class ObjectIdentifier():
    
    def __init__(self):
        file_path = config.__poject_dir__+ "data/nlp_engine/ner_training/classifier.pickle"
        if(os.path.isfile(file_path)):
            classifier_file = open(file_path , "rb")
            clf = pickle.load(classifier_file)
            self.clf = clf
            classifier_file.close()
        else :
            self.clf = Pipeline([
                ('vectorizer', DictVectorizer(sparse=False)),
                ('classifier', DecisionTreeClassifier(criterion='entropy'))
                ])   

    def tag(self,sentence):
        history = []
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        iob_tags = self.clf.predict([features(tagged,count,history) for count,gibberish in enumerate(tagged)])
        complete_token = to_standard_form(tokens,tagged,iob_tags)
        return complete_token

    
    def train(self,X,Y):
        self.clf.fit(X,Y)
        file_path = config.__poject_dir__+ "data/nlp_engine/ner_training/classifier.pickle"
        classifier_file = open(file_path,"ab")
        pickle.dump(self.clf,classifier_file)
        classifier_file.close()
        
        
    
    def accuracy(self,X_test,Y_test):
        score = self.clf.score(X_test,Y_test)
        return score
   
        
        
