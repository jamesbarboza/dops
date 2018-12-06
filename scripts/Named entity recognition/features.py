

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

