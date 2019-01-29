import sys
sys.path.append("../..")
import pickle
import project_config as config
import nltk
from libs.models.File import File
from libs.nlp_engine.VoteClassifier import VoteClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier

training_path = config.__training_dir__ + "hashtags/"

file_obj = File()
files = file_obj.getTrainingFiles(training_path, "")

#print(files)
"""
hashtag_category = {
	"politics" : [],
	"business" : []
}

"""
"""
hashtag_category = {}

for (path, file) in files:
	category = path.replace("__", "")
	file_path = training_path + category + "/" + file
	hashtag_file = open(file_path, "rb")
	hashtags = pickle.load(hashtag_file)

	if category in hashtag_category:
		hashtags_in_category = hashtag_category[category]
		for hashtag in hashtags:
			if hashtag in hashtags_in_category:
				for i,x in enumerate(hashtags_in_category):
					if x == hashtag:
						del(hashtags_in_category[i])

		hashtag_category[category] = hashtags_in_category
	else:
		hashtag_category[category] = hashtags
"""

categories = {}
all_hashtags = []

for (path, file) in files:
	category = path.replace("__", "")
	file_path = training_path + category + "/" + file
	file = open(file_path, "rb")
	hashtags_in_file = pickle.load(file)
	all_hashtags = list(set(all_hashtags + hashtags_in_file))
	file.close()
	if category in categories:
		hashtags_in_category = categories[category]
		hashtags_in_category = list(set(hashtags_in_category + hashtags_in_file))
		catgories[category] = hashtags_in_category
	else:
		categories[category] = hashtags_in_file

print(len(categories))

def find_features(hashtags):
	features = {}
	for ht in all_hashtags:
		features[ht] = (ht in hashtags)
	return features

feature_set = []

for (path, file) in files:
	category = path.replace("__", "")
	file_path = training_path + category + "/" + file
	file = open(file_path, "rb")
	hashtags_in_file = pickle.load(file)
	feature_set.append( (find_features(hashtags_in_file), category) )
	file.close()

#print(feature_set)
training_set = feature_set
testing_set = [ "#metoo", "#sabrimala", "#charitytuesday" ]
testing_set = [ "#business" ]

#Simple Naive Bayes Algorithm
naive_bayes_classifier = nltk.NaiveBayesClassifier.train(training_set)
#print("Accuracy: ", nltk.classify.accuracy(naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/hashtag/naive_bayes.pkl", "wb")
pickle.dump(naive_bayes_classifier, file)
file.close()

#Multinomial Naive Bayes Algorithm
multinomial_naive_bayes_classifier = SklearnClassifier(MultinomialNB())
multinomial_naive_bayes_classifier.train(training_set)
#print("Algorithm: Multinomial Naive Bayes", "Accuracy:", nltk.classify.accuracy(multinomial_naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/hashtag/multinomial_naive_bayes.pkl", "wb")
pickle.dump(multinomial_naive_bayes_classifier, file)
file.close()

#Bernoulli Naive Bayes Algorithm
bernoulli_naive_bayes_classifier = SklearnClassifier(BernoulliNB())
bernoulli_naive_bayes_classifier.train(training_set)
#print("Algorithm: Bernoulli Naive Bayes", "Accuracy:", nltk.classify.accuracy(multinomial_naive_bayes_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/hashtag/bernoulli_naive_bayes.pkl", "wb")
pickle.dump(bernoulli_naive_bayes_classifier, file)
file.close()

#Logistic Regression Algorithm
logistic_regression_classifier = SklearnClassifier(LogisticRegression())
logistic_regression_classifier.train(training_set)
#print("Algorithm: Logistic Regression", "Accuracy:", nltk.classify.accuracy(logistic_regression_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/hashtag/logistic_regression.pkl", "wb")
pickle.dump(logistic_regression_classifier, file)
file.close()

#Stochastic Gradient Descent Algorithm
sgdc_classifier = SklearnClassifier(SGDClassifier())
sgdc_classifier.train(training_set)
#print("Algorithm: Stochastic Gradient Descent", "Accuracy:", nltk.classify.accuracy(sgdc_classifier, testing_set) * 100)
file = open(config.__project_dir__ + "data/nlp_engine/document_classifications/hashtag/stochastic_gradient_descent.pkl", "wb")
pickle.dump(sgdc_classifier, file)
file.close()

voted_classifier = VoteClassifier(
    naive_bayes_classifier,
    multinomial_naive_bayes_classifier,
    bernoulli_naive_bayes_classifier,
    logistic_regression_classifier,
    sgdc_classifier
)

def hashtag_classification(hashtags):
    feats = find_features(hashtags)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

print(hashtag_classification(testing_set))