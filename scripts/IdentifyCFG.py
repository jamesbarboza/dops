import nltk


def get_tokens(pos_tagged_tokens,tags):
	nouns = []
	for count,tagged in enumerate(pos_tagged_tokens):
		word , pos_tag = tagged 
		if pos_tag == (tags):
			nouns.append(word)
	return nouns
tokens = [('I', 'PRP'), ('shot', 'VBP'), ('an', 'DT'), ('elephant', 'NN'), ('in', 'IN'), ('my', 'PRP$'), ('pajamas', 'NN')]

grammer = nltk.CFG.fromstring("""
	S -> NP  VP
	PP -> P NP
	NP -> Det N | Det N PP 
	VP -> V NP | VP PP
	NP -> 'get_tokens(tokens,"NN")'
	""")