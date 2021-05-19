# -*- coding: utf-8 -*-
# 
# Spectral Analysis Clustering Explorer (SpACE)
# Missouri State University
# CSC450 Fall 2020 - Dr. Razib Iqbal
#
# Team 2 (FTIR/ECOSTRESS/SpACE team):
# Austin Alvidrez
# Brad Meyer
# Collin Tinen
# Kegan Moore
# Sam Nack
#
# Copyright 2020 Austin Alvidrez, Brad Meyer, Collin Tinen,
# Kegan Moore, Sam Nack
#
# Spectral Analysis Clustering Explorer (SpACE) is free software:
# you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spectral Analysis Clustering Explorer (SpACE) is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with Spectral Analysis Clustering Explorer (SpACE).
# If not, see <https://www.gnu.org/licenses/>.

# space_dbscan.py
# This file contains function related to the DBSCAN algorithm.
#
# Includes: DBSCAN clustering, calculate cluster
# composition, 2D plotting, 3D plotting.

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


# linked to functional requirement #2 - DBSCAN clustering algorithm
# Compute DBSCAN
def do_dbscan(epsilon, minimum, dataset):
    """
    This function accepts values for epsilon and MinPts (minimum)
    and a combined pandas dataframe of shape n_samples x n_features.
    It fits the dataset, and returns a dbscan object.
    """
    db = DBSCAN(eps=epsilon, min_samples=minimum).fit(dataset)
    return db


# linked to functional requirement #2 - DBSCAN clustering algorithm
# linked to functional requirement #12 - calculate cluster of composition
# Compute cluster composition
def db_comp(db, data_objects, sort_category):
    """
    This function accepts a dbscan object, a list of data objects, and
    a category to sort by and calculates the composition of each cluster.
    It returns a pandas dataframe with the composition of each cluster.
    Composition dataframe is of shape clusters x categories.
    Each row is a cluster, and each column is a category.
    """
    labels = list(map(lambda x: x + 1, db.labels_))
    comp = pd.DataFrame(index=range(len(set(labels))))
    comp.index.name = "Cluster No."
    for i in range(len(data_objects)):
        split_file_name = data_objects[i].filename.split(".")
        category = split_file_name[0]
        if sort_category > 1:
            category = category + "." + split_file_name[1]
            if sort_category > 2:
                category = category + "." + split_file_name[2]
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[labels[i], category] = 1
        else:
            comp.at[labels[i], category] += 1

    return comp


# linked to functional requirement #11 - visualize clustered data
# linked to non-functional requirement #2 - perform visualization in under 5 minutes
# linked to non-functional requirement #6 - support up to 100 different colors for visualization
def plot2D(dataset, db, embedded=False, master=None):
    """
    This function takes a combined pandas dataframe and a dbscan object.
    It plots the DBSCAN clusters in 2D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the function returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI.
    """
    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot()
    else:
        figure, axes = plt.subplots()

    # dbscan labels contain some -1s, which is wreaking havoc,
    # so let's change -1 to 0 and shift all other labels by +1
    # e.g. -1 becomes 0, 0 becomes 1, 1 becomes 2...
    plot_labels = []
    for label in db.labels_:
        plot_labels.append(label + 1)

    # now, fix our colormap so that the first color (for 0, the new
    # noise points) is black
    colormap = cm.get_cmap('viridis')(np.linspace(0, 1, 101))
    black = [0, 0, 0, 1]

    # if there is noise, add black to the colormap and set n_clusters to labels - 1, else do not
    if 0 in plot_labels:
        new_colors = np.insert(colormap, 0, black, axis=0)
        new_colormap = ListedColormap(new_colors)
        n_clusters = len(set(plot_labels)) - 1
    else:
        new_colormap = ListedColormap(colormap)
        n_clusters = len(set(plot_labels))

    scatter = axes.scatter(x=dataset[0], y=dataset[1], c=plot_labels, cmap=new_colormap, picker=True)

    handles, labels = scatter.legend_elements(num=n_clusters if n_clusters > 0 else "auto")
    axes.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1),
                title="Cluster #\n(0=Noise)", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, columnspacing=3,
                edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None


# linked to functional requirement #11 - visualize clustered data
# linked to non-functional requirement #2 - perform visualization in under 5 minutes
# linked to non-functional requirement #6 - support up to 100 different colors for visualization
def plot3D(dataset, db, embedded=False, master=None):
    """
    This function takes a combined pandas dataframe and a dbscan object.
    It plots the DBSCAN clusters in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the function returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI.
    """
    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot(111, projection="3d")
    else:
        figure, axes = plt.subplots(subplot_kw={"projection": "3d"})

    # dbscan labels contain some -1s, which is wreaking havoc,
    # so let's change -1 to 0 and shift all other labels by +1
    # e.g. -1 becomes 0, 0 becomes 1, 1 becomes 2...
    plot_labels = []
    for label in db.labels_:
        plot_labels.append(label + 1)

    # now, fix our colormap so that the first color (for 0, the new
    # noise points) is black
    colormap = cm.get_cmap('viridis')(np.linspace(0, 1, 101))
    black = [0, 0, 0, 1]

    # if there is noise, add black to the colormap, else do not
    if 0 in plot_labels:
        new_colors = np.insert(colormap, 0, black, axis=0)
        new_colormap = ListedColormap(new_colors)
        n_clusters = len(set(plot_labels)) - 1
    else:
        new_colormap = ListedColormap(colormap)
        n_clusters = len(set(plot_labels))

    scatter = axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=plot_labels, cmap=new_colormap,picker=True)

    handles, labels = scatter.legend_elements(num=n_clusters if n_clusters > 0 else "auto")
    axes.legend(handles, labels, loc='upper left', bbox_to_anchor=(1.1, 1),
                title="Cluster #\n(0=Noise)", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, columnspacing=3,
                edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None
