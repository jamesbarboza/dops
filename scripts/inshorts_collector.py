from urllib.request import urlopen
from bs4 import BeautifulSoup
import nltk
import re
import requests
import json
import os
import sys
sys.path.append("..")
import project_config as config
os.chdir(config.__training_dir__)

category = "technology"
domain = "https://inshorts.com"
url = "https://inshorts.com/en/read/" + category

#	Read the page from the url
#html_page = urlopen(url).read()

html_file = open("/home/xkid/projects/playground/data/inshorts_html", "r")
html_page = html_file.read()
html_file.close()

#	Use the BeautifulSoup class to arrange and find tags
soup = BeautifulSoup(html_page, "html.parser")

#	Find all divs with the clas
divs = soup.findAll("div", { "class" : "news-card" })

folders = os.listdir()

if category not in folders:
	os.mkdir(category)
	os.chdir(category)
else:
	os.chdir(category)

for div in divs:
	title = div.find("span", { "itemprop" : "headline"}).text
	content = div.find("div", { "itemprop" : "articleBody" }).text

	filename = title + ".txt"
	filecontent = title + "\n\n" + content
	files = os.listdir()
	if filename not in files:
		with open(filename, "w") as file:
			file.write(filecontent)