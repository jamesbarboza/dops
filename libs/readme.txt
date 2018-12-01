--------------------------------------------------------------------------------------------------------------------------------
WordTagger usage

1. "Data/Training Set- Word Tagger/" has 2 pickle files -
	features - which contains features extracted from 100676 words of Treebank corpus
	target - which has pos tags of words of Treebank corpus 

2. tag = Tagger(t) #creating instance of class
3. tag.train(X,Y) # X is features , Y is target ,load the pickle files and extract respective list from it 
4. tag.pos_tag("Pickle is God") 
--------------------------------------------------------------------------------------------------------------------------------