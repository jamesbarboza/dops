import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
import dops.project_config as config

class MultinomialNBClassifier():

    def __init__(self):
        f = open(config.__project_dir__ + "data/nlp_engine/document_classifications/classifiers/multinomial_nb.pkl", "rb")
        self.classifier = pickle.load(f)
        f.close()
    
    def find_features(self, text):
        f = open(config.__project_dir__ + "data/nlp_engine/document_classifications/features.pkl", "rb")
        word_features = pickle.load(f)
        f.close()
        features = {}
        doc_words = word_tokenize(text)
        for word in word_features:
            features[word] = (word in doc_words)
        return features
    
    def classify(self, text):
        feats = self.find_features(text)
        result = self.classifier.classify(feats)
        return result