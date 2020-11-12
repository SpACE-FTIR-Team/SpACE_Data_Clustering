import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# Compute DBSCAN
def do_dbscan(epsilon, minimum, dataset):
    db = DBSCAN(eps=epsilon, min_samples=minimum).fit(dataset)
    return db

# Compute cluster composition
def db_comp(db, data_objects, sort_category):
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    comp = pd.DataFrame(index=range(n_clusters))
    if -1 in labels:
        comp.append([-1])
    for i in range(len(data_objects)):
        if sort_category in data_objects[i].descriptive.descriptor.values:
            category = data_objects[i].descriptive.\
                loc[data_objects[i].descriptive['descriptor'] == sort_category, 'value'].iloc(0)[0].upper()
        else:
            category = "None specified"
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[labels[i], category] = 1
        else:
            comp.at[labels[i], category] += 1
        
    return comp

def plot2D(dataset, db, embedded=False):
    """Attempt to write a 2D DBSCAN plot that is the same as K-means,
    so we can then figure out how to modify it like K-means to plot 3D."""
    figure, axes = plt.subplots()

    db = db.fit(dataset)  # refit to reduced data for plotting
    # dbscan labels contain some -1s, which is wreaking havoc,
    # so let's change -1 to 0 and shift all other labels by +1
    # e.g. -1 becomes 0, 0 becomes 1, 1 becomes 2...
    plot_labels = []
    for label in db.labels_:
        plot_labels.append(label + 1)

    # now, fix our colormap so that the first color (for 0, the new
    # noise points) is black
    colormap = cm.get_cmap('plasma')(np.linspace(0, 1, 101))
    black = [0, 0, 0, 1]
    new_colors = np.insert(colormap, 0, black, axis=0)
    new_colormap = ListedColormap(new_colors)

    axes.scatter(x=dataset[0], y=dataset[1], c=plot_labels, cmap=new_colormap)

    if embedded:
        return figure
    else:
        plt.show()
        return None


def plot3D(dataset, db, embedded=False):
    figure, axes = plt.subplots(subplot_kw={"projection": "3d"})

    db = db.fit(dataset)  # refit to reduced data for plotting
    # dbscan labels contain some -1s, which is wreaking havoc,
    # so let's change -1 to 0 and shift all other labels by +1
    # e.g. -1 becomes 0, 0 becomes 1, 1 becomes 2...
    plot_labels = []
    for label in db.labels_:
        plot_labels.append(label + 1)

    # now, fix our colormap so that the first color (for 0, the new
    # noise points) is black
    colormap = cm.get_cmap('plasma')(np.linspace(0, 1, 101))
    black = [0, 0, 0, 1]
    new_colors = np.insert(colormap, 0, black, axis=0)
    new_colormap = ListedColormap(new_colors)

    axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=plot_labels, cmap=new_colormap)

    if embedded:
        return figure
    else:
        plt.show()
        return None
