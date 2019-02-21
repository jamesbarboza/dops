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

#################################################
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

db = DBSCAN(eps=20, min_samples=10).fit(d)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(l, labels))
print("Completeness: %0.3f" % metrics.completeness_score(l, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(l, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(l, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(l, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(d, labels))


import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = d[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = d[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()