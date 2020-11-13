import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    for i in range(len(data_objects)):
       
        category = data_objects[i].descriptive.\
            loc[data_objects[i].descriptive['descriptor'] == sort_category, 'value'].iloc(0)[0].upper()
        if labels[i] == -1:
            continue
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[labels[i], category] = 1
        else:
            comp.at[labels[i], category] += 1
        
    return comp

def plot2D(dataset, db, embedded=False, master=None):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the funtion returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI."""

    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot()
    else:
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
        return canvas
    else:
        plt.show()
        return None


def plot3D(dataset, db, embedded=False, master=None):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the funtion returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI."""

    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot(111, projection="3d")
    else:
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
        return canvas
    else:
        plt.show()
        return None
