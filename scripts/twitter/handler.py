from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import datetime

import sys
sys.path.append("../..")
import project_config as config

class Listener(StreamListener):
	def on_data(self, data):
		tweet_data = json.loads(data)
		data_to_write = tweet_data['text'] + "\n\n"
		print(data_to_write)

		timestamp = datetime.datetime.now()
		today = timestamp.strftime('%d%m%y')

		with open(config.__training_dir__ + 'tech_and_startup/twitter' + today +'.txt', 'a') as twitter_file:
			twitter_file.write(data_to_write)

	def on_error(self, status):
		print(status)
		if status == 420:
			return False

auth = OAuthHandler(config.capi, config.capi_secret)
auth.set_access_token(config.ctoken, config.ctoken_secret)

twitter_stream = Stream(auth, Listener())

#keywords = ["USA", "Donald Trump", "Mauro Viale", "politics"]
keywords = [ "tech", "technology", "startup", "innovation"]
twitter_stream.filter(track=keywords)