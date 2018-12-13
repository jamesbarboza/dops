import sys
sys.path.append("../..")
import pickle

import project_config as config
from libs.nlp_engine.VoteClassifier import VoteClassifier

file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/wordfeatures.pkl", "rb")
word_features = pickle.load(file)
file.close()

def find_features(doc_words):
	features = {}
	for word in word_features:
		features[word] = (word in doc_words)
	return features

#naive_bayes
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/naive_bayes.pkl", "rb")
classifier_nb = pickle.load(file)
file.close()

#multinomial
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/multinomial_naive_bayes.pkl", "rb")
classifier_mnb = pickle.load(file)
file.close()

#bernoulli
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/bernoulli_naive_bayes.pkl", "rb")
classifier_bnb = pickle.load(file)
file.close()

#linearregression
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/logistic_regression.pkl", "rb")
classifier_lr = pickle.load(file)
file.close()

#stochasticgradientdescent
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/stochastic_gradient_descent.pkl", "rb")
classifier_sgd = pickle.load(file)
file.close()

voted_classifier = VoteClassifier(
    classifier_nb,
    classifier_mnb,
    classifier_bnb,
    classifier_lr,
    classifier_sgd
)

def category_classification(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)


sent = input("Enter a statement")
print(category_classification(sent))