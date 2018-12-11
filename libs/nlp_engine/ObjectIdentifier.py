import re
import sys
sys.path.append("../..")
import nltk
import string
import os
import os.path
import collections
import pickle
import project_config as config


from collections import Iterable
from nltk.corpus import conll2000
from nltk.chunk import conlltags2tree,tree2conlltags,ChunkParserI
from nltk.tag import ClassifierBasedTagger
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline


from libs.models.File import File
from libs.models.RawFile import RawFile

from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from libs.nlp_engine.VoteClassifier import VoteClassifier







class ObjectIdentifier():
    
    def __init__(self):
        file_path = config.__project_dir__+ "data/nlp_engine/ner_training/classifier.pickle"
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
        iob_tags = self.clf.predict([self.features(tagged,count,history) for count,gibberish in enumerate(tagged)])
        complete_token = self.to_standard_form(tokens,tagged,iob_tags)
        return complete_token

    
    def train(self,X,Y):
        self.clf.fit(X,Y)
        file_path = config.__project_dir__+ "data/nlp_engine/ner_training/classifier.pickle"
        classifier_file = open(file_path,"ab")
        pickle.dump(self.clf,classifier_file)
        classifier_file.close()
        
        
    
    def accuracy(self,X_test,Y_test):
        score = self.clf.score(X_test,Y_test)
        return score
        #array [ 'IOB','IOB'] to (word , pos-tag ,IOB)
    
    def to_standard_form(self,tokens,pos_tag,iob):
        standard_form = []
        for i in range(len(tokens)):
            standard_form.append((tokens[i],pos_tag[i][1],iob[i]))
        return standard_form

    def transform_into_dataset(self,untagged_words,history):
        X = []
        Y = history
        for count,tagged in enumerate(untagged_words):
            X.append(self.features(self,untagged_words,count,history))
        return X,Y

    def features(self,tagged_sentence,index,history):
        tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + list(tagged_sentence) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
        history = ['[START2]', '[START1]'] + list(history)
        index = index + 2 
        word = tokens[index][0]
        pos_tag = tokens[index][1]
        length_of_word = len(word)
        shape = word.isnumeric()
        is_titled = word.istitle()
        is_uppercase = word.isupper()
        is_lowercase = word.islower()

        prev_word = tokens[index-1][0]
        prev_word_pos_tag = tokens[index-1][1]
        
        precedes_IN = 'true' if tokens[index-1][1] == "IN" else 'false'

        prev_prev_word = tokens[index-2][0]
        prev_prev_word_pos_tag = tokens[index-2][1]
        
        next_VERB = 'true' if tokens[index+1][1] == "VBD"  else 'false'

        next_word =  tokens[index+1][0]
        next_word_pos_tag = tokens[index+1][1]
        next_next_word = tokens[index+2][0]
        next_next_word_pos_tag = tokens[index+2][1]    

        
        #prev_IOB = tagged_sentence[i][j][1]
        

        '''
        frequency = fdist[word]
        prefix = check_prefix()
        suffix = check_suffix()
        
        existence_dictionary = does_it_mean()
        '''
    
        return {
        'word': word,
        #'lemma': stemmer.stem(word),
        'pos-tag': pos_tag ,
        #'all-ascii': allascii,
 
        'next-word': next_word,
        #'next-lemma': stemmer.stem(nextword),
        'next-pos': next_word_pos_tag,
 
        'next-next-word': next_next_word,
        'nextnextpos': next_next_word_pos_tag,
 
        'prev-word': prev_word,
        #'prev-lemma': stemmer.stem(prevword),
        'prev-pos': prev_word_pos_tag,
 
        'prev-prev-word': prev_prev_word,
        'prev-prev-pos': prev_prev_word_pos_tag,
 
        #'prev-iob': previob,
 
        'contains-dash': 'false' if word.find("-") == -1  else 'true',
        'contains-dot': 'false' if word.find(".") == -1  else 'true',
 
        'all-caps': is_uppercase,
        'is-title': is_titled,
        'is-lower': is_lowercase,
 
        'prev-all-caps': prev_word.isupper(),
         #'prev-capitalized': prevcapitalized,
 
        'next-all-caps': next_word.isupper(),
        #'next-capitalized': nextcapitalized,
        }



   
        
        
