import nltk
import math 
from nltk import word_tokenize,sent_tokenize
from nltk.probability import FreqDist

import sys
import project_config as config
from libs.models.Dictionary import Dictionary
from libs.models.RawFile import RawFile
from libs.models.File import File

class LexicalAnalyzer:
    
    def __init__(self):
        print("Initializing..")
        #self.tokenize()
        #self.tagging()
        self._files = []

    #   convert the given text to sentences
    def toSentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    #   convert the given text to words
    def toWords(self, text):
        words = nltk.word_tokenize(text)
        return words

##    def tokenize(self):
##        temp_words = []
##        words = []
##        sentences = []
##        syllables = []
##        all_words = []
##
##        for i in range(len(self.paragraphs_list)):
##            sentences.append(nltk.sent_tokenize(self.paragraphs_list[i]))
##            for j in range(len(sentences[i])):
##                temp_words.append(nltk.word_tokenize(sentences[i][j]))
##                words.append(nltk.word_tokenize(sentences[i][j]))
##            syllables.append((self.paragraphs_list[i],sentences[i],temp_words[0:len(temp_words)]))
##            temp_words.clear()        
##
##        for i in range (len(words)):
##            for w  in words[i]:
##                all_words.append(w)
##
##    
##        self.sentences = sentences
##        self.words = words
##        self.all_words = all_words
##        self.syllables = syllablest

         

    def largest_word(self,tokens):
        largest_word = tokens[0]
        for i in range(1,len(tokens)):
            compare=tokens
            if(len(largest_word)<len(compare)):
                largest_word = compare

        return largest_word
    

    def average_len_of_words(self,tokens):
        no_of_words = len(tokens)
        sum_of_length_words =0
        for i in range(len(tokens)):
            sum_of_length_words += len(tokens[i])
                
        avg = (sum_of_length_words/no_of_words)
        ceil = math.ceil(avg)
        floor = math.floor(avg)
        
        if((avg-ceil)>(floor-avg)):
            avg = floor
        else :
            avg = ceil

        return avg

    def get_paragraphs(rawtext):
        return [w for w in ((paragraph.strip()).split("\n")) if w != ""]

    def get_sentences(rawtext):
        sents = []
        sents.append(nltk.sent_tokenize(rawtext))
        return sents

    def get_words(rawtext):
        words = []
        words.append(nltk.word_tokenize(rawtext))
        return words

    def pos_tag(tokenized_words):
        tagged_words =[]
        tagged_words.append(nltk.pos_tag(tokenized_words))
        return tagged_words

    def FreqDist(tokens):
        fdist = FreqDist(tokens)
        return fdist


    def lexical_diversity(tokens):
        return len(set(tokens))/len(tokens)



    

          
