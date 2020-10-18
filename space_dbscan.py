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
      dataset = StandardScaler().fit_transform(dataset)
      db = DBSCAN(eps=epsilon, min_samples=minimum).fit(dataset)
      return db
      

# #############################################################################
# Plot 2D result
def plot2D(db, dataset):
      labels = db.labels_
      colors = [plt.cm.Spectral(each)
                  for each in np.linspace(0, 1, len(labels))]
      
      cx = []
      cy = []

      for i in labels:
            cx.append(0)
            cy.append(1)
      plt.scatter(x=dataset[0], y=dataset[1], c=labels, cmap='tab20')
      plt.scatter(x=cx, y=cy, color="black", s=50)
  
      plt.show() 