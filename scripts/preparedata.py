import csv
import sys
sys.path.append("..")
from libs.learn.PrepareData import PrepareTextualData

data = []

with open("/home/xkid/projects/data/csv/analytics_tweet.csv", "r") as f:
    raw = csv.reader(f)
    for row in raw:
        data.append([ row[0], row[2] ])

td = data
pd = PrepareTextualData()
pd.prepare(td)
d,l = pd.getPreparedData()
print(type(d))
print(l)

import matplotlib.pyplot as plt
plt.plot(d, "ro")
plt.show()