import nltk
import math 
from nltk import word_tokenize,sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet
import re
import sys
import project_config as config
from libs.models.Dictionary import Dictionary
from libs.models.RawFile import RawFile
from libs.models.File import File

class LexicalAnalyzer:
    
    def __init__(self):
        self._file_content = ""

    #   load file content from the given file path
    def load(self, file_path):
        raw_file = RawFile()
        raw_file.load(file_path)
        file_content = raw_file.read()
        self._file_content = str(file_content['content']['content'])

    #   load file content from the given text
    #   no raw file instance needed
    def loadText(self, text):
        self._file_content = str(text)

    #   convert the given text to sentences
    def toSentences(self):
        sentences = nltk.sent_tokenize(self._file_content)
        return sentences

    #   convert the given text to words
    def toWords(self):
        words = nltk.word_tokenize(self._file_content)
        return words

    #   get the lexical diversity of the text
    #   the text is provided with either the load() or loadText() methods
    def lexicalDiversity(self):
        words = self.toWords()
        total_words = len(words)
        distinct_words = list(set(words))
        return distinct_words/total_words

    #   define part of speech (pos) for every word and return
    #   returned value should be a list in the format [(), (), ... ()]
    def wordsToPos(self):
        return nltk.pos_tag(nltk.word_tokenize(self._file_content))

    def frequencyDistribution(self):
        return FreqDist(self.toWords())

    #   get synonym of a particular word
    def getSynonym(self, word, pos):
        synonyms = []
        syn_name = word + "." + pos
        synsets = wordnet.synsets(word)
        similarity_score = 0
        synset_names = []
        for syn in synsets:
            synset_name = str(syn.name())
        
        for syn in syns:
            syn_score = synset.wup_similarity(str(syn.name()))
            if syn_score > score:
                score = syn_score
                synonyms = [l.name() for l in s.lemmas()]

        return synonyms
        

    #   get antonyms of a particular word
    def getAntonym(self, word):
        antonyms = []

        syns = wordnet.synsets(word)
        for s in synsets:
            for l in s.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        return antonyms