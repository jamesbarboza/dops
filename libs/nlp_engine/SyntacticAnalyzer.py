import nltk
import pickle
import re
from .LexicalAnalyzer import LexicalAnalyzer
from .ObjectIdentifier import ObjectIdentifier
import dops.project_config as config

class ComplexityTree:
	__data = None
	__leftNode = None
	__rightNode = None

	def __init__(self, data):
		self.__data = data

	def setData(self, data):
		self.__data = data

	def getData(self):
		return self.__data
	
	def setLeftNode(self, node):
		self.__leftNode = node

	def setRightNode(self, node):
		self.__rightNode = node

	def getLeftNode(self):
		return self.__leftNode

	def getRightNode(self):
		return self.__rightNode

	def printTree(self):
		if self.getLeftNode():
			self.getLeftNode().printTree()
		print(self.getData())
		if self.getRightNode():
			self.getRightNode().printTree()


class SyntacticAnalyzer(LexicalAnalyzer):

	def __init__(self):
		super(SyntacticAnalyzer, self).__init__()

	#	Method to pick out three word phrases
	#	eg: "Expected to arrive"
	#	Can be used in many ways
	def getTrigrams(self, text):
		phrases=[]
		sentences = nltk.sent_tokenize(text)
		pos_tagged_sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences]
		#print(pos_tagged_sentences)
		for sent in pos_tagged_sentences:
			for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sent):
				print(w1,w2,w3)
				if (t1.startswith('V') and t2 == 'TO' and t3.startswith('V')):
					phrases.append((w1,w2,w3))
					#print(w1,w2,w3)

		return phrases

	#	The police accused the thief, "He robbed the bank".
	#	Check if the sentence is a direct speech or not
	#	return boolean True/False and the quote if True
	def isDirectSpeech(self, sentence):
		verbs_before_quotes = []
		
		double_quote = re.findall(r'"(.*)"', sentence)
		single_quote = re.findall(r"'(.*)'", sentence)
		quote = ""
		if len(double_quote) > 0:
			quote = double_quote[0]
			sentence = re.sub(r'"(.*)"', '', sentence)
		elif len(single_quote) > 0:
			quote = single_quote[0]
			sentence = re.sub(r"'(.*)'", "", sentence)
		
		with open(config.__project_dir__ + "data/nlp_engine/speech/words_before_quotes", "rb") as f:
			verbs_before_quotes = pickle.load(f)
		
		verbs = [ word for (word,tag) in nltk.pos_tag(nltk.word_tokenize(sentence)) if "VB" in tag ]
		for verb in verbs:
			if verb.lower() in verbs_before_quotes:
				return True, quote

		return false

	#	If any of the verb in the sentence is found in the indirect speech wordlist
	#	return True
	def inDirectSpeech(self, sentence):
		verbs_before_quotes = []
		with open(config.__project_dir__ + "data/nlp_engine/speech/words_before_quotes", "rb") as f:
			verbs_before_quotes = pickle.load(f)
		
		for verb in verbs_before_quotes:
			if verb in sentence:
				return True
		
	#	eg: "To find nemo that's missing"
	#	return aim if found
	def getStatementObjectiveIfExists(self, sentence):
		aim = ""
		aim_mutex = 0
		tokens = nltk.word_tokenize(sentence)
		pos_tagged_tokens = nltk.pos_tag(tokens)
		for (word, tag) in pos_tagged_tokens:
			if aim_mutex > 0:
				aim += word + " "
			if tag == 'TO':
				aim_mutex = 1
				aim += word + " "
		return aim.strip()

	#	Check if the sentence is complex
	#	if True, split the statement with the help of complexwords
	#	Store the subordination conjunctions in a stack and return the stack as well
	def complexStatement(self, sentence):
		complexwords = []
		cTree = None
		with open(config.__project_dir__ + "data/nlp_engine/speech/complexwords", "rb") as f:
			complexwords = pickle.load(f)

		tokens = nltk.word_tokenize(sentence)
		for token in tokens:
			if token in complexwords:
				cTree = ComplexityTree(token)
				sentence = sentence.split(token)
				break

		if type(sentence) is list:
			cTree.setLeftNode(self.complexStatement(sentence[0].strip()))
			cTree.setRightNode(self.complexStatement(sentence[1].strip()))
			return cTree
		else:
			cTree = ComplexityTree(sentence.strip())
			return cTree

	#	Check if the sentence is compound
	#	if True, split the statemnt with the help of compoundwords
	def compoundStatement(self, sentence):
		compoundwords = []
		cTree = None
		with open(config.__project_dir__ + "data/nlp_engine/speech/compoundwords", "rb") as f:
			compoundwords = pickle.load(f)

		tokens = nltk.word_tokenize(sentence)
		for token in tokens:
			if token in compoundwords:
				cTree = ComplexityTree(token)
				sentence = sentence.split(token)
				break
		
		if type(sentence) is list:
			cTree.setLeftNode(self.compoundStatement(sentence[0].strip()))
			cTree.setRightNode(self.compoundStatement(sentence[1].strip()))
			return cTree
		else:
			cTree = ComplexityTree(sentence)
			return cTree

	def complexityTree(self, sentence):
		words = []
		ctree = None
		with open(config.__project_dir__ + "data/nlp_engine/speech/complexwords", "rb") as f:
			complexwords = pickle.load(f)
			words += complexwords

		with open(config.__project_dir__ + "data/nlp_engine/speech/compoundwords", "rb") as f:
			compoundwords = pickle.load(f)
			words += compoundwords

		tokens = nltk.word_tokenize(sentence)

		for token in tokens:
			if token in words:
				cTree = ComplexityTree(token)
				sentence = sentence.split(token)
				break
		
		if type(sentence) is list:
			cTree.setLeftNode(self.complexityTree(sentence[0].strip()))
			cTree.setRightNode(self.complexityTree(sentence[1].strip()))
			return cTree
		else:
			cTree = ComplexityTree(sentence.strip())
			return cTree
