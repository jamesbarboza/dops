import sys
sys.path.append("../..")
import random
import pickle
import nltk

import project_config as config
from libs.models.File import File
from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from libs.nlp_engine.SyntacticAnalyzer import SyntacticAnalyzer
from libs.nlp_engine.VoteClassifier import VoteClassifier

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier

file_obj = File()
files = file_obj.getTrainingFiles(config.__training_dir__, "")

all_words = []
for (path, file) in files:
	file_path = config.__training_dir__ + path.replace("__", "/") + "/" + file
	print(file_path)
	lex = LexicalAnalyzer()
	lex.load(file_path)

	file_words = lex.wordsToPos()
	
	#	list of tags to reject
	reject_tags = [ 'TO', 'DT', 'IN', 'LS', 'MD', 'CC', 'PDT', 'PRP', 'UH', "'", ",", ".", "(", ")", ":" ]
	for (word, tag) in file_words:
		if tag not in reject_tags:
			all_words.append(word)

frequency_dist = nltk.FreqDist(all_words)

word_features = list(frequency_dist.keys())[:5000]

file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/wordfeatures.pkl", "wb")
pickle.dump(word_features, file)
file.close()

def find_features(doc_words):
	features = {}
	for word in word_features:
		features[word] = (word in doc_words)
	return features

feature_set = []
for (path, file) in files:
	category = path
	file_path = config.__training_dir__ + path.replace("__", "/") + "/" + file
	lex = LexicalAnalyzer()
	lex.load(file_path)
	feature_set.append( (find_features(lex.toWords()), category) )

random.shuffle(feature_set)

training_set = feature_set
testing_set = feature_set[7:]

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