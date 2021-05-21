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

# space_kmeans.py
# This file contains function related to the KMeans algorithm.
#
# Includes: K-means clustering, calculate cluster
# composition, 2D plotting, 3D plotting.

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# linked to functional requirement #1 - kmeans clustering algorithm
def do_Kmeans(num_clusters, dataset):
    """
    This function accepts an integer number of clusters and
    a combined pandas dataframe of shape n_samples x n_features.
    It fits the dataset, and returns a kmeans object which has
    attributes that describe the cluster centroids,
    and which cluster each sample is in.
    """
    kmeans = KMeans(n_clusters=num_clusters).fit(dataset)
    return kmeans


# linked to functional requirement #1 - kmeans clustering algorithm
# linked to functional requirement #12 - calculate cluster composition
def calculate_composition(km, num_clusters, data_objects, sort_category):
    """
    This function accepts a kmeans object, a number of clusters,
    a list of data objects, and a category to sort by and calculates
    the composition of each cluster.
    It returns a pandas dataframe with the composition of each cluster.
    Composition dataframe is of shape clusters x categories.
    Each row is a cluster, and each column is a category.
    """

    comp = pd.DataFrame(index=range(num_clusters))
    comp.index.name = "Cluster No."
    for i in range(len(data_objects)):
        # access the value where descriptor == sort_category
        split_file_name = data_objects[i].filename.split(".")
        category = split_file_name[0]
        if sort_category > 1:
            category = category + "." + split_file_name[1]
            if sort_category > 2:
                category = category + "." + split_file_name[2]
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[km.labels_[i], category] = 1
        else:
            comp.at[km.labels_[i], category] += 1

    return comp

def do_comprehensive(cluster, dobjs):
    col_names = ["Filename","Cluster No.","Type","Type.Class","Type.Class.Subclass","Additional Information"]
    df = pd.DataFrame(columns=col_names)
    for i, dobj in enumerate(dobjs):
        new_row = [dobj.filename, cluster.labels_[i]]
        split_name = dobj.filename.split(".")
        type = split_name[0]
        tc = type + "." + split_name[1]
        tcsc = tc + "." + split_name[2]
        new_row.append(type)
        new_row.append(tc)
        new_row.append(tcsc)
        new_row.append(cluster.cluster_centers_[i])
        zipped_row = dict(zip(col_names, new_row))
        df = df.append(zipped_row,ignore_index=True)
    return df


# linked to functional requirement #11 - visualize clustered data
# linked to non-functional requirement #2 - perform visualization in under 5 minutes
# linked to non-functional requirement #6 - support up to 100 different colors for visualization
def plot2D(dataset, km, embedded=False, master=None):
    """
    This function takes a combined pandas dataframe and a kmeans object.
    It plots the K-means clusters and centroids in 2D.
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

    cx = []
    cy = []
    km = km.fit(dataset)  # refit to reduced data for centroids
    for i in km.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
    scatter = axes.scatter(x=dataset[0], y=dataset[1], c=km.labels_, cmap="viridis", picker=True)
    axes.scatter(x=cx, y=cy, marker="x", color="black", s=50)

    handles, labels = scatter.legend_elements(num=(km.n_clusters if km.n_clusters % 2 == 0 else
                                                   km.n_clusters - 1))
    axes.legend(handles, labels,
                ncol=(2 if km.n_clusters > 50 else 1),
                loc='upper left', bbox_to_anchor=(1, 1),
                title="Cluster #", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None


# linked to functional requirement #11 - visualize clustered data
# linked to non-functional requirement #2 - perform visualization in under 5 minutes
# linked to non-functional requirement #6 - support up to 100 different colors for visualization
def plot3D(dataset, km, embedded=False, master=None):
    """
    This function takes a combined pandas dataframe and a kmeans object.
    It plots the K-means clusters and centroids in 3D.
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

    cx = []
    cy = []
    cz = []
    km = km.fit(dataset)  # refit to reduced data for centroids
    for i in km.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
        cz.append(i[2])
    scatter = axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=km.labels_, cmap="viridis", picker=True)
    axes.scatter3D(xs=cx, ys=cy, zs=cz, marker="x", color="black", s=50)

    handles, labels = scatter.legend_elements(num=(km.n_clusters if km.n_clusters % 2 == 0 else
                                                   km.n_clusters - 1))
    axes.legend(handles, labels,
                ncol=(2 if km.n_clusters > 50 else 1),
                loc='upper left', bbox_to_anchor=(1.1, 1),
                title="Cluster #", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None
