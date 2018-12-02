import re
import nltk
import string
import os
import collections

from collections import Iterable
from nltk.corpus import conll2000
from nltk.chunk import conlltags2tree,tree2conlltags,ChunkParserI
from nltk.tag import ClassifierBasedTagger
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline



ner_tags = collections.Counter()


corpus_root = "gmb-1.0.0"

#function modify IOB tags, changing first occurence of I to B. 
def to_iob_form(gmb_form):
    iob_form = []
    for count,gmb_token in enumerate(gmb_form) :
        word, pos_tag, ner_tag = gmb_token
        
        if ner_tag != 'O':
            
            if count == 0 :
                ner_tag = "B-" + ner_tag.split('-')[1]
            elif gmb_form[count-1][2] == ner_tag :
                ner_tag = "I-" + ner_tag.split('-')[1]
            else:
                ner_tag = "B-" + ner_tag.split('-')[1]

        iob_form.append((word,pos_tag,ner_tag))

    return iob_form

#[(word,pos,ner)] to [((word,pos),ner)]
def to_nltk_form(gmb_form):
    nltk_form = []
    for count,gmb_token in enumerate(gmb_form) :
        word, pos_tag, ner_tag = gmb_token
        nltk_form.append(((word,pos_tag),ner_tag))
    return nltk_form

def untag(iob_form):
    untagged = []
    for count,gmb_token in enumerate(iob_form):
        word, pos_tag,ner_tag = gmb_token
        untagged.append((word,pos_tag))
    return untagged 
    
def history(iob_form):
    history = []
    for count,gmb_token in enumerate(iob_form) :
        word, pos_tag,ner_tag = gmb_token
        history.append(ner_tag)
    return history 

#reading gmb tokens and converting to standard form [(word,pos,ner)]
def read_corpus(corpus_root):
    standard_tokens = []
    for root,dirs,files in os.walk(corpus_root):
        for filename in files:
            if filename.endswith(".tags"):
                with open(os.path.join(root,filename),'rb') as file_handle :
                    file_content = file_handle.read().decode('utf-8').strip()
                    training_sentences = file_content.split('\n\n')
                    for training_sentence in training_sentences:
                        training_tokens =[word for word in training_sentence.split('\n') if word]
                        for training_token in training_tokens:
                
                            tag = training_token.split('\t')
                            word, pos_tag = tag[0],tag[1]

                            #if corpus is gmb 1.0.0
                            ner_tag = tag[4].split('\n')[0]
        
                            #splitting and taking only primary tags if corpus is gmb 2.2.0
                            '''

                            if ner_tag != 'O':
                                ner_tag = ner_tag.split('-')[0]
                            if pos_tag in ('LQU', 'RQU'):
                                pos_tag = "``"
                            '''    

                            ner_tags[ner_tag] += 1
                            standard_tokens.append((word,pos_tag,ner_tag))
                            
                        
       
    return standard_tokens


def transform_into_dataset(untagged_words,history):
    X = []
    Y = []

    for count,tagged in enumerate(untagged_words):
        
        X.append(features(untagged_words,count,history))
        
        
    return X

def features(tagged_sentence,index,history):
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + list(tagged_sentence) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)
    index = index + 2 
    word = tokens[index][0]
    pos_tag = tokens[index][1]
    length_of_word = len(word)
    shape = word.isnumeric()
    is_titled = word.istitle()
    is_uppercase = word.isupper()
    is_lowercase = word.islower()

    prev_word = tokens[index-1][0]
    prev_word_pos_tag = tokens[index-1][1]
        
    precedes_IN = 'true' if tokens[index-1][1] == "IN" else 'false'

    prev_prev_word = tokens[index-2][0]
    prev_prev_word_pos_tag = tokens[index-2][1]
        
    next_VERB = 'true' if tokens[index+1][1] == "VBD"  else 'false'

    next_word =  tokens[index+1][0]
    next_word_pos_tag = tokens[index+1][1]
    next_next_word = tokens[index+2][0]
    next_next_word_pos_tag = tokens[index+2][1]    

        
    #prev_IOB = tagged_sentence[i][j][1]
        

    '''
        frequency = fdist[word]
        prefix = check_prefix()
        suffix = check_suffix()
        
        existence_dictionary = does_it_mean()
        '''
    
    return {
    'word': word,
    #'lemma': stemmer.stem(word),
    'pos-tag': pos_tag ,
    #'all-ascii': allascii,
 
    'next-word': next_word,
    #'next-lemma': stemmer.stem(nextword),
    'next-pos': next_word_pos_tag,
 
    'next-next-word': next_next_word,
    'nextnextpos': next_next_word_pos_tag,
 
    'prev-word': prev_word,
    #'prev-lemma': stemmer.stem(prevword),
    'prev-pos': prev_word_pos_tag,
 
    'prev-prev-word': prev_prev_word,
    'prev-prev-pos': prev_prev_word_pos_tag,
 
    #'prev-iob': previob,
 
    'contains-dash': 'false' if word.find("-") == -1  else 'true',
    'contains-dot': 'false' if word.find(".") == -1  else 'true',
 
    'all-caps': is_uppercase,
    'is-title': is_titled,
    'is-lower': is_lowercase,
 
    'prev-all-caps': prev_word.isupper(),
     #'prev-capitalized': prevcapitalized,
 
    'next-all-caps': next_word.isupper(),
    #'next-capitalized': nextcapitalized,
    }

    
                                      

class ner_clf():
    
    def __init__(self,features,target):
        self.clf = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', DecisionTreeClassifier(criterion='entropy'))
            ])   

    def tag(self,sentence):
        history = []
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        iob_tags = self.clf.predict([features(tagged,count,history) for count,gibberish in enumerate(tagged)])
        complete_token = self.to_standard_form(tokens,tagged,iob_tags)
        return complete_token

    #array [ 'IOB','IOB'] to (word , pos-tag ,IOB)
    def to_standard_form(self,tokens,pos_tag,iob):
        standard_form = []
        for i in range(len(tokens)):
            standard_form.append((tokens[i],pos_tag[i][1],iob[i]))
        return standard_form
        

    def train(self,X,Y):
        self.clf.fit(X,Y)
    
    def accuracy(self,X_test,Y_test):
        score = self.clf.score(X_test,Y_test)
        return score
   
        
        
