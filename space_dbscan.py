print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import cm
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler



# #############################################################################
# Compute DBSCAN
def do_dbscan(epsilon, minimum, dataset):
      db = DBSCAN(eps=epsilon, min_samples=minimum).fit(dataset)
      return db
      

# #############################################################################
# Plot result
def plot_dbscan(db, dataset):
      core_sample_mask = np.zeros_like(db.labels_, dtype=bool)
      core_sample_mask[db.core_sample_indices_] = True
      labels = db.labels_


      #Get Num of clusters in labels. Ignore any noise.
      n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
      n_noise = list(labels).count(-1)

      unique_labels = set(labels)
      colors = [plt.cm.Spectral(each)
                  for each in np.linspace(0,1, len(unique_labels))]
      for k, col in zip(unique_labels, colors):
            if k == -1:
                  col = [0, 0, 0, 1]
            class_member_mask = (labels == k)

            xy = dataset[class_member_mask & core_sample_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                        markeredgecolor='k', markersize=14)
            xy = dataset[class_member_mask & ~core_sample_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                        markeredgecolor='k', markersize=6)
      
      plt.show()