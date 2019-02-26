import re
import nltk
import pickle
import sys

import dops.project_config as config
from dops.libs.models.Dictionary import Dictionary
from dops.libs.models.RawFile import RawFile

class SyntacticAnalyzer():
	def __init__(self):
		#self.nouns = self.getNouns(lexicalAnalyzer)
		#self.verbs = self.getVerbs(lexicalAnalyzer)
		self.adjectives = []
		self.adverbs = []
		self.unsimplified_tags = []


	#	Method to get list of nouns
	def getNouns(self, lexicalAnalyzer):
		nouns = [(a,b) for (a,b) in lexicalAnalyzer.pos_tagged_distinct if re.search(r'^NN*', b, re.I)]
		return nouns

	#	Method to get list of verbs
	def getVerbs(self, lexicalAnalyzer):
		verbs = [(a,b) for (a,b) in lexicalAnalyzer.pos_tagged_distinct if re.search(r'^V*', b, re.I)]
		return verbs

	#	Method to pick out three word phrases
	#	eg: "Expected to arrive"
	#	Can be used in many ways
	def threeWordsPhrases(self, lexicalAnalyzer):
		phrases=[]
		parargraphs = lexicalAnalyzer.paragraphs_list
		for paragraph in parargraphs:
			#print(paragraph)
			sentences = nltk.sent_tokenize(paragraph)
			pos_tagged_sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]
			#print(pos_tagged_sentences)
			for sent in pos_tagged_sentences:
				for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sent):
					if (t1.startswith('V') and t2 == 'TO' and t3.startswith('V')):
						phrases.append((w1,w2,w3))
						print(w1,w2,w3)

		return phrases

	#	Final method to save dictionary
	#	take processed dictionary data and filename as input parameters
	#	should be saved as binary
	def saveDictionary(self, dictionary, filename):
		with open(config.__project_dir__ + "data/nlp_engine/document_classifications/" + filename, "wb") as file:
			pickle.dump(dictionary, file)

	#	Method to load the dictionary from data
	#	dictionary should be read in binary
	def loadDictionary(self, filename):
		with open(config.__project_dir__ + "data/nlp_engine/document_classifications/" + filename, "rb") as file:
			loaded_dictionary = pickle.load(file)
			#print(type(loaded_dictionary))
			return loaded_dictionary

	#	Method to aggregrate the data on a particular dictionary
	#	Take data as dictionary and filename, filename is the storage location
	#	If dictionary doesn't exist then create
	def addToDictionary(self, dictionary, filename):
		try:
			with open(config.__project_dir__ + "data/nlp_engine/document_classifications/" + filename, "rb") as file:
				data = pickle.load(file)
				dictionary_to_save = data['dictionary']
				for (key, value) in dictionary:
					if key in dictionary:
						dictionary_value = dictionary_to_save[key]
						dictionary_value = (dictionary_value + value) / 2
						dictionary_to_save[key] = dictionary_value
					else:
						dictionary_to_save[key] = value

				data['iterator'] = data['iterator'] + 1
				data['dictionary'] = dictionary_to_save
		except IOError:
			print("Error")
			data = {
				'iterator': 1,
				'dictionary': {}
			}
			dictionary_to_save = data['dictionary']
			for (key, value) in dictionary:
				dictionary_to_save[key] = value

			data['dictionary'] = dictionary_to_save
		self.saveDictionary(data, filename)
