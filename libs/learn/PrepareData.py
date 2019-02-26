"""
Take the data in the form of 
[
    [1, abcd, abcd, y],
    [2, xyz, xyz, b],
]

#convert the above to numpy.array for further processing

array([
    [],
    [],
])

USAGE:

text_data = PrepareTextualData()
text_data.prepare(input_data)
data = text_data.getPreparedData()
"""

import numpy as np
from dops.libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from nltk.corpus import stopwords
import nltk

stop_words = set(stopwords.words('english'))

class PrepareTextualData:
    __subjects = []
    __predicates = []
    __processed_data = []
    __labels = []

    def __init__(self):
        print("Initialized")

    def prepare(self, data):
        lex = LexicalAnalyzer()
        for row in data:
            data_to_add = []    # [ subject, predicate ]
            feature_data = row[0]
            self.__labels.append(row[1])
            
            subject, predicate = lex.getSubjectAndPredicate(feature_data)

            words_in_subject = nltk.word_tokenize(subject)
            words_in_predicate = nltk.word_tokenize(predicate)

            tagged_subjects_words = nltk.pos_tag(words_in_subject)
            tagged_predicate_words = nltk.pos_tag(words_in_predicate)

            subject = ""
            for (word, tag) in tagged_subjects_words:
                if not word.lower() in stop_words:
                    subject += word.strip() + " "          
            
            predicate = ""
            for (word, tag) in tagged_predicate_words:
                if not word.lower() in stop_words:
                    predicate += word.strip() + " "

            subject = subject.strip()
            predicate = predicate.strip()

            if not subject in self.__subjects:
                self.__subjects.append(subject)

            if not predicate in self.__predicates:
                self.__predicates.append(predicate)

            data_to_add = [ subject, predicate ]
            self.__processed_data.append(data_to_add)
        
        self.__subjects = sorted(self.__subjects)
        self.__predicates = sorted(self.__predicates)
        self.valueSubstitution()

    def valueSubstitution(self):
        data = []
        for row in self.__processed_data:
            subject = 0
            predicate = 0
            if row[0]:
                for i in range(len(self.__subjects)):
                    if row[0] == self.__subjects[i]:
                        subject = i+1
            else:
                subject = 0
            if row[1]:
                for i in range(len(self.__predicates)):
                    if row[1] == self.__predicates[i]:
                        predicate = i+1
            else:
                predicate = 0
            data.append([subject, predicate])
        self.__processed_data = data
        

    def getPreparedData(self):
        data = np.array(self.__processed_data)
        labels = np.array(self.__labels)
        return data, labels