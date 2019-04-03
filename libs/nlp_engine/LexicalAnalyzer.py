import nltk
import math
from nltk import word_tokenize,sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet
import re
import sys
import dops.project_config as config
from dops.libs.models.Dictionary import Dictionary
from dops.libs.models.RawFile import RawFile
from dops.libs.models.File import File
import urllib.parse

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

    #   find hashtags in a given sentence
    #   return empty list if no hashtag found
    def findHashtags(self, sentence):
        hashtags = []
        words = nltk.word_tokenize(sentence)
        for i in range(len(words)):
            hashtag = ""
            try:
                if words[i] == "#":
                    hashtag += words[i] + words[i+1]
                    hashtags.append(hashtag)
            except:
                print("error has occurred")
        return hashtags

    #   return subject and predicate of the given sentence
    #   check for VB VBD VBP VBZ tags
    def getSubjectAndPredicate(self, sentence):
        subject = ""
        predicate = ""
        subject_mutex = 0

        words = nltk.word_tokenize(str(sentence))
        tokens = nltk.pos_tag(words)

        for (word, tag) in tokens:
            if subject_mutex > 0:
                predicate += word + " "
            else:
                if tag == "VB" or tag == "VBD" or tag == "VBP" or tag == "VBZ":
                    predicate += word + " "
                    subject_mutex = 1
                else:
                    subject += word + " "

        return subject, predicate

    #   convert to url to basic http url
    #   HTTPS changes to HTTP, remove GET variables
    def basic_url(self, url):
        url = urllib.parse.unquote(url)
        url = re.sub(r'https', 'http', url)
        url = re.sub(r'\?(.)*', '', url)
        return url
