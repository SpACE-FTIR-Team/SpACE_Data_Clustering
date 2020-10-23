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

# #############################################################################
# Plot 3D result
def plot3D(db, dataset):
      figure, axes = plt.subplots(subplot_kw={"projection": "3d"})
      labels = db.labels_
      cx = []
      cy = []
      cz = []

      for i in labels:
            cx.append(0)
            cy.append(1)
            cz.append(2)
      axes.scatter3D(xs=dataset[0],ys=dataset[1], zs=dataset[2],
                    c=labels, cmap="tab20")
      axes.scatter3D(xs=cx, ys=cy, zs=cz, color="black", s=50)

      plt.show() 