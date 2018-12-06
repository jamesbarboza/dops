import os
import pickle 
import collections
import classification
import features
from classification import *
from features import *



#converting GMB corpus's token into compatible nltk tokens for training



#reading gmb tokens and converting to standard form [(word,pos,ner)]
ner_tags = collections.Counter()

def get_dataset(start_index,end_index,corpus_root):
    file_path = "C:/Users/Vabs/DOPS/dops -not git/Data/GMB 2.2.0/ner_chunks.pickle"
    if(os.path.isfile(file_path)):
        file = open(file_path , 'rb')
        iob_tokens = pickle.load(file)
    else:
       gmb_tokens = read_gmb(corpus_root)
       iob_tokens = to_iob_form(gmb_tokens)
       
    iob_tokens = iob_tokens[start_index : end_index]
    untagged_tokens = untag(iob_tokens)
    history_tokens = history(iob_tokens)
    X = transform_into_dataset(untagged_tokens ,history_tokens)
    Y = history_tokens
    return X,Y
    

#use the following method to read gmb 2.2.0 corpus
def read_gmb(corpus_root):
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
                            ner_tag = tag[3].split('\n')[0]
        
                            #splitting and taking only primary tags if corpus is gmb 2.2.0
                            
                            if ner_tag != '0':
                                ner_tag = ner_tag.split('-')[0]
                                
                            if pos_tag in ('LQU', 'RQU'):
                                pos_tag = "``"
                            
                            ner_tags[ner_tag] += 1
                            standard_tokens.append((word,pos_tag,ner_tag))
                            
                        
       
    return standard_tokens

# Adding IOB tags B, O, I in NER tags
def to_iob_form(gmb_form):
    iob_form = []
    for count,gmb_token in enumerate(gmb_form) :
        word, pos_tag, ner_tag = gmb_token
        ner_tag = ner_tag.upper()
        if ner_tag != 'O':
            
            if count == 0 :
                ner_tag = "B-" + ner_tag
            elif gmb_form[count-1][2] == ner_tag :
                ner_tag = "I-" + ner_tag
            else:
                ner_tag = "B-" + ner_tag

        iob_form.append((word,pos_tag,ner_tag))

    return iob_form


#[(word,pos,ner)] to [((word,pos),ner)]
def to_nltk_form(iob_form):
    nltk_form = []
    for count,iob_token in enumerate(iob_form) :
        word, pos_tag, ner_tag = iob_token
        nltk_form.append(((word,pos_tag),ner_tag))
    return nltk_form


# Removing ner tag from (word,pos_tag,ner_tag) 
def untag(iob_form):
    untagged = []
    for count,gmb_token in enumerate(iob_form):
        word, pos_tag,ner_tag = gmb_token
        untagged.append((word,pos_tag))
    return untagged 

# extracting only ner tag from training data (word , pos_tag , ner_tag)
def history(iob_form):
    history = []
    for count,gmb_token in enumerate(iob_form) :
        word, pos_tag,ner_tag = gmb_token
        history.append(ner_tag)
    return history 




def transform_into_dataset(untagged_words,history):
    X = []
    Y = []

    for count,tagged in enumerate(untagged_words):
        
        X.append(features(untagged_words,count,history))
        
        
    return X


