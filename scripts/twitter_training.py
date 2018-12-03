import sys
import nltk
import math
import random
import pickle
import csv

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier

sys.path.append("..")

import project_config as config
from libs.models.File import File
from libs.models.RawFile import RawFile

from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from libs.nlp_engine.VoteClassifier import VoteClassifier

# load files
# create lexical model
# out lexical analysis
print("Initializing...")

rawfile = RawFile()
rawfile.load(config.__project_dir__ + "data/nlp_engine/training/news/News_Category_Dataset.json")
raw_objects = rawfile.read()

#categories = [ raw_object['category'] for raw_object in raw_objects]
#categories = list(set(categories))

categories = [ "POLITICS", "WORLD NEWS", "MEDIA", "SPORTS", "CRIME"]
all_words = []

data = []
lexical = LexicalAnalyzer()
counter = 0
for raw_object in raw_objects:
    if raw_object['category'] in categories:
        data.append(raw_object)
        headline = raw_object['headline']
        description = raw_object['short_description']
        content = headline + description
        words = lexical.toWords(content)
        all_words += words
        counter += 1
        print(counter)

frequency_dist = nltk.FreqDist(all_words)
word_features = list(frequency_dist.keys())[:math.ceil(len(categories)/2) * 100]

#add world cup players to the word features
file = open("../data/nlp_engine/training/sports/fifa_world_cup/WorldCupPlayers.csv", "r")
csv_data = csv.reader(file, delimiter=",")
rows = [row for row in csv_data]
rows = [21000:]
counter = 0
for row in rows:
    word_features += nltk.word_tokenize(row[0])
    word_features += nltk.word_tokenize(row[1])
    counter += 1
    print(counter)
file.close()

print("Created Frequency Distribution")

def find_features(document):
    document_words = list(set(nltk.word_tokenize(document)))
    words = {}
    for word in document_words:
        words[word] = word

    features = {}
    for word in word_features:
        features[word] = (word in words)
    return features

#feature_set = [(find_features(raw_object['headline'] + raw_object['short_description']), raw_object['category']) for raw_object in data]
feature_set = []
counter = 0
for raw_object in data:
    feature_set.append((find_features(raw_object['headline'] + " " + raw_object['short_description']), raw_object['category']))
    counter += 1
    print(counter)

for row in rows:
    feature_set.append((find_features(row[0] + " " + row[1]),row[2]))

random.shuffle(feature_set)

training_set = feature_set
testing_set = feature_set[58000:]

print("Training and testing set created")
print("Classifying...")

#Simple Naive Bayes Algorithm
naive_bayes_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Accuracy: ", nltk.classify.accuracy(naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/naive_bayes.pkl", "wb")
pickle.dump(naive_bayes_classifier, file)
file.close()

#Multinomial Naive Bayes Algorithm
multinomial_naive_bayes_classifier = SklearnClassifier(MultinomialNB())
multinomial_naive_bayes_classifier.train(training_set)
print("Algorithm: Multinomial Naive Bayes", "Accuracy:", nltk.classify.accuracy(multinomial_naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/multinomial_naive_bayes.pkl", "wb")
pickle.dump(multinomial_naive_bayes_classifier, file)
file.close()

#Bernoulli Naive Bayes Algorithm
bernoulli_naive_bayes_classifier = SklearnClassifier(BernoulliNB())
bernoulli_naive_bayes_classifier.train(training_set)
print("Algorithm: Bernoulli Naive Bayes", "Accuracy:", nltk.classify.accuracy(multinomial_naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/bernoulli_naive_bayes.pkl", "wb")
pickle.dump(bernoulli_naive_bayes_classifier, file)
file.close()

#Logistic Regression Algorithm
logistic_regression_classifier = SklearnClassifier(LogisticRegression())
logistic_regression_classifier.train(training_set)
print("Algorithm: Logistic Regression", "Accuracy:", nltk.classify.accuracy(logistic_regression_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/logistic_regression.pkl", "wb")
pickle.dump(logistic_regression_classifier, file)
file.close()

#Stochastic Gradient Descent Algorithm
sgdc_classifier = SklearnClassifier(SGDClassifier())
sgdc_classifier.train(training_set)
print("Algorithm: Stochastic Gradient Descent", "Accuracy:", nltk.classify.accuracy(sgdc_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/stochastic_gradient_descent.pkl", "wb")
pickle.dump(sgdc_classifier, file)
file.close()

voted_classifier = VoteClassifier(
    naive_bayes_classifier,
    multinomial_naive_bayes_classifier,
    bernoulli_naive_bayes_classifier,
    logistic_regression_classifier,
    sgdc_classifier
)

print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)

def category_classification(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

print(category_classification("Cristiano ronaldo expertly scored a goal"))