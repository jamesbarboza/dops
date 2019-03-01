import pickle
from nltk.corpus import stopwords
import dops.project_config as config
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import re
from nltk.stem import WordNetLemmatizer

class SGDClassifier():
    def __init__(self):
        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/classifiers/sgdc.pkl", "rb")
        self.classifier = pickle.load(f)
        f.close()

    def classify(self, text):
        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/features.pkl", "rb")
        documents = pickle.load(f)
        f.close()

        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/labels.pkl", "rb")
        y = pickle.load(f)
        f.close()

        document = text
        stemmer = WordNetLemmatizer()
        document = re.sub(r'\W', ' ', document)
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        document = re.sub(r'^b\s+', '', document)
        document = document.lower()
        document = document.split()
        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)
        documents.append(document)

        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(documents).toarray()

        tfidfconverter = TfidfTransformer()
        X = tfidfconverter.fit_transform(X).toarray()

        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(documents).toarray()

        X_test = [X[len(X)-1]]
        result = self.classifier.predict(X_test)
        return result


class DecisionTree():
    def __init__(self):
        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/classifiers/decision_tree.pkl", "rb")
        self.classifier = pickle.load(f)
        f.close()

    def classify(self, text):
        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/features.pkl", "rb")
        documents = pickle.load(f)
        f.close()

        f = open(config.__project_dir__ + "data/nlp_engine/sentence_classification/labels.pkl", "rb")
        y = pickle.load(f)
        f.close()

        document = text
        stemmer = WordNetLemmatizer()
        document = re.sub(r'\W', ' ', document)
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        document = re.sub(r'^b\s+', '', document)
        document = document.lower()
        document = document.split()
        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)
        documents.append(document)

        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(documents).toarray()

        tfidfconverter = TfidfTransformer()
        X = tfidfconverter.fit_transform(X).toarray()

        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(documents).toarray()

        X_test = [X[len(X)-1]]
        result = self.classifier.predict(X_test)
        return result