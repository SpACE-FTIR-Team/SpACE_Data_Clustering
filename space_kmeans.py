# -*- coding: utf-8 -*-
"""
This is a temporary kmeans clustering file
"""
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt


def do_Kmeans(num_clusters, dataset):
    """This function accepts a integer number of clusters and a pandas dataframe of shape n_samples x n_features it
    fits the dataset, and returns a kmeans object which has attributes that describe the cluster centroids,
    and which cluster each sample is in """
    kmeans = KMeans(n_clusters=num_clusters).fit(dataset)
    return kmeans


def calculate_composition(km, num_clusters, data_objects):
    """This function accepts a kmeans object, a number of clusters and a list of data objects and calculates the
    composition of each cluster, it returns a pandas dataframe with the composition of each cluster.  Composition
    dataframe is of shape clusters x categories. Each row is a cluster, and each column is a category """
    comp = pd.DataFrame(index=range(num_clusters))
    for i in range(len(data_objects)):
        category = data_objects[i].descriptive.loc[data_objects[i].descriptive['descriptor'] == 'Type', 'value'][1].upper()
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[km.labels_[i], category] = 1
        else:
            comp.at[km.labels_[i], category] += 1

    return comp


def plot3D(dataset, clusters, embedded=False):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window and the function returns None.
    If embedded is True, the function returns a Figure object
    to be displayed on a FigureCanvasTkAgg embedded in the GUI."""
    figure, axes = plt.subplots(subplot_kw={"projection": "3d"})
    cx = []
    cy = []
    cz = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
        cz.append(i[2])
    axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=clusters.labels_, cmap="tab20")
    axes.scatter3D(xs=cx, ys=cy, zs=cz, marker="x", color="blue", s=50)
    if embedded:
        return figure
    else:
        plt.show()
        return None


def plot2D(dataset, clusters, embedded=False):
    """This function plots clusters and cluster centers in 2D.
    If embedded is False, the the plot is displayed in a standalone
    modal window and the function returns None.
    If embedded is True, the function returns a Figure object
    to be displayed on a FigureCanvasTkAgg embedded in the GUI."""
    figure, axes = plt.subplots()
    cx = []
    cy = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
    axes.scatter(x=dataset[0], y=dataset[1], c=clusters.labels_, cmap="tab20")
    axes.scatter(x=cx, y=cy, marker="x", color="black", s=50)
    if embedded:
        return figure
    else:
        plt.show()
        return None
