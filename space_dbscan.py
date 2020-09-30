print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
dataset, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

dataset = StandardScaler().fit_transform(dataset)

# #############################################################################
# Compute DBSCAN
def do_dbscan(dataset):
      db = DBSCAN(eps=0.3, min_samples=10).fit(dataset)

# #############################################################################
# Plot result
       
      y_pred = db.fit_predict(dataset)
      plt.scatter(dataset[:,0],
      dataset[:,1], c = y_pred, cmap='Paired')
      plt.title("DBSCAN")
      plt.show()

if __name__ == "__main__":
      do_dbscan(dataset)