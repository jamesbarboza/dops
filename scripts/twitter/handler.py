from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

import sys
sys.path.append("../..")
import project_config as config

class Listener(StreamListener):
	def on_data(self, data):
		tweet_data = json.loads(data)
		print(tweet_data['text'])


	def on_error(self, status):
		print(status)

auth = OAuthHandler(config.capi, config.capi_secret)
auth.set_access_token(config.ctoken, config.ctoken_secret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track=["USA", "Donald Trump", "Mauro Viale", "politics"])