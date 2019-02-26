from nltk.classify import ClassifierI
from statistics import mode
import pickle
import dops.project_config as config

class VoteClassifier(ClassifierI):

    def __init__(self):
        self._classifiers = []
        
        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/naive_bayes.pkl", "rb")
        naive_bayes = pickle.load(file)
        self._classifiers.append(naive_bayes)
        file.close

        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/multinomial_naive_bayes.pkl", "rb")
        multinomial_nb = pickle.load(file)
        self._classifiers.append(multinomial_nb)
        file.close()

        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/bernoulli_naive_bayes.pkl", "rb")
        bernoulli_ng = pickle.load(file)
        self._classifiers.append(bernoulli_ng)
        file.close()

        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/bernoulli_naive_bayes.pkl", "rb")
        logistic_regression = pickle.load(file)
        self._classifiers.append(logistic_regression)
        file.close()

        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/bernoulli_naive_bayes.pkl", "rb")
        sgdc = pickle.load(file)
        self._classifiers.append(sgdc)
        file.close()


    def classify(self, text):
        votes = []
        doc_features = self.find_features(text)
        for classifier in self._classifiers:
            vote = classifier.classify(doc_features)
            votes.append(vote)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(features)
            votes.append(vote)
        
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def find_features(self, doc_words):
        file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/wordfeatures.pkl", "rb")
        word_features = pickle.load(file)
        file.close()
        features = {}
        for word in word_features:
            features[word] = (word in doc_words)
        return features