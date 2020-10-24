import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# Compute DBSCAN
def do_dbscan(epsilon, minimum, dataset):
    # TODO: research StandardScaler and if we need it
    dataset = StandardScaler().fit_transform(dataset)
    db = DBSCAN(eps=epsilon, min_samples=minimum).fit(dataset)
    return db


# Plot 2D result
def plot2D(dataset, db, embedded=False):
    figure, axes = plt.subplots()

    db = db.fit(dataset)  # refit to reduced data for plotting
    labels = db.labels_  # dbscan labels represent the cluster each index belongs to
    unique_labels = set(labels)  # get number of unique labels (equal to number of clusters + 1 for noise)
    colors = [plt.get_cmap('nipy_spectral')(each)  # colors for each cluster and noise
              for each in np.linspace(0, 1, len(unique_labels))]
    samples_mask = np.zeros_like(db.labels_, dtype=bool)  # create an array of booleans to represent the labels
    samples_mask[db.core_sample_indices_] = True  # match booleans to index of clusters
    set_np = dataset.to_numpy()  # DataFrame to NumPy array conversion for index slicing

    for k, color in zip(unique_labels, colors):
        if k == -1:
            color = [0, 0, 0, 1]  # black for noise

        class_mask = (labels == k)  # array of booleans to match clusters

        xy = set_np[class_mask & samples_mask]
        axes.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
                 markeredgecolor='k', markersize=14)

        # ~samples_mask = samples_mask inverted
        xy = set_np[class_mask & ~samples_mask]
        axes.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
                 markeredgecolor='k', markersize=6)

    if embedded:
        return figure
    else:
        plt.title('DBSCAN')
        plt.show()
        return None



# TODO: Plot 3D result
# Currently not functional
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
    axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2],
                   c=labels, cmap="tab20")

    plt.show()
