import nltk
import sklearn
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

import sys
sys.path.append("../..")
import dops.project_config as config


class WordTagger:
    def __init__(self,tokenized_sentence):
        self.clf = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', DecisionTreeClassifier(criterion='entropy'))
            ])
 
    def train(self,X,Y):
        self.clf.fit(X,Y)
        

    def features(self,sentence,index):
        """ sentence: [w1, w2, ...], index: the index of the word """
        word = sentence[index]
        return {
            'word': word,
            'is_first': 'true' if index == 0 else 'false',
            'is_last': 'true' if index == len(sentence)-1 else 'false',
            'is_title': word.istitle(),
            'is_all_caps': word.isupper(),
            'is_all_lower': word.islower(),
            'prefix-1': sentence[index][0],
            'prefix-2': sentence[index][:2],
            'prefix-3': sentence[index][:3],
            'suffix-1': sentence[index][-1],
            'suffix-2': sentence[index][-2:],
            'suffix-3': sentence[index][-3:],
            'prev_word': sentence[index-1] if index != 0 else "",
            'next_word': sentence[index+1] if index != len(sentence) - 1 else "",
            'has_hyphen': '-' in word,
            'is_numeric': word.isdigit(),
            'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
            }
    
    def untag(self,tagged_sentences):
        untagged = []
        for i in range(len(tagged_sentences)):
            untagged.append(tagged_sentences[i][0])

        return untagged



    def transform_to_dataset(self,tagged_sentences):
        X = []
        y = []

        for index ,tagged in enumerate(tagged_sentences):

            X.append(self.features((self.untag(tagged_sentences)),index))
            y.append(tagged_sentences[index][1])
            
        return X, y

    def pos_tag(self,sentence):
        tokenized = nltk.word_tokenize(sentence)
        tags = self.clf.predict([self.features(tokenized, index) for index in range(len(tokenized))])
        return (sentence, tags)

    def accuracy(self,X_test,Y_test):
        score = self.clf.score(X_test,Y_test)
        print("Accuracy",score)
    
