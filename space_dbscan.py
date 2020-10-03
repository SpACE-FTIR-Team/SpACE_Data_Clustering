print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
dataset, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

dataset = StandardScaler().fit_transform(dataset)

# #############################################################################
# Compute DBSCAN
def do_dbscan(dataset):
      db = DBSCAN(eps=0.3, min_samples=10).fit(dataset)
      core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
      core_samples_mask[db.core_sample_indices_] = True
      labels = db.labels_

      # Number of clusters in labels, ignoring noise if present.
      n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
      n_noise_ = list(labels).count(-1)

# #############################################################################
# Plot result
      
      unique_labels = set(labels)     
      colors = [plt.cm.Spectral(each)
            for each in np.linspace(0, 1, len(unique_labels))]
      for k, col in zip(unique_labels, colors):
            if k == -1:
                  # Black used for noise.            
                  col = [0, 0, 0, 1]

            class_member_mask = (labels == k)

            xy = dataset[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                  markeredgecolor='k', markersize=14)

            xy = dataset[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                  markeredgecolor='k', markersize=6)

      plt.show()

if __name__ == "__main__":
      do_dbscan(dataset)