from libs.models.database.MySQLModel import MySQLModel
from libs.models.Dictionary import Dictionary
from libs.models.File import File
from libs.models.RawFile import RawFile

from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer
from libs.nlp_engine.SyntacticAnalyzer import SyntacticAnalyzer
from libs.nlp_engine.WordTagger import WordTagger
from libs.nlp_engine.VoteClassifier import VoteClassifier

print("hello world")

word_tagger = WordTagger()
word_tagger.pos_tag("Hello world")