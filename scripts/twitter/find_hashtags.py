from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import datetime
import pickle

import sys
sys.path.append("../..")
import project_config as config
import os

from libs.nlp_engine.LexicalAnalyzer import LexicalAnalyzer

class Listener(StreamListener):
	def on_data(self, data):
		tweet_data = json.loads(data)
		text = tweet_data['text']
		lex = LexicalAnalyzer()
		hashtags = lex.findHashtags(text)
 
		timestamp = datetime.datetime.now()
		today = timestamp.strftime('%d%m%y')

		#category = "politics"
		category = "business"
		
		path = config.__training_dir__ + 'hashtags/' + category + '/' + today

		if os.path.isfile(path):
			if os.path.getsize(path) > 0:
				file = open(path, "rb")
				data = pickle.load(file)
				file.close()
				file = open(path, "wb")
				for hashtag in hashtags:
					if not hashtag in data:
						data.append(hashtag)
						print(hashtag)
				pickle.dump(data, file)
				file.close()
		else:
			file = open(path, "wb")
			pickle.dump(hashtags, file)
			file.close()

	def on_error(self, status):
		print(status)
		if status == 420:
			return False

auth = OAuthHandler(config.capi, config.capi_secret)
auth.set_access_token(config.ctoken, config.ctoken_secret)

twitter_stream = Stream(auth, Listener())

#keywords = ["USA", "Donald Trump", "Mauro Viale", "politics"]
#keywords = [ "USA", "politics"]
keywords = [ "USA", "business"]
twitter_stream.filter(track=keywords)