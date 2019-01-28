from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
import nltk

text = "That, was a great game."
tagged_tokens = nltk.pos_tag(nltk.word_tokenize(text))

for (word, pos) in tagged_tokens:
	if pos == 'NN':


lex = LexicalAnalyzer()
synonym = lex.getSynonym("even")
print(synonym)