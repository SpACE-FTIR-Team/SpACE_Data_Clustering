# -*- coding: utf-8 -*-
"""
This is a temporary kmeans clustering file
"""

from sklearn.cluster import KMeans
import space_random_data
import pandas as pd


def do_Kmeans(num_clusters, dataset):
    """This function accepts a integer number of clusters and a pandas dataframe of shape n_samples x n_features
    it fits the dataset, and returns a kmeans object which has attributes that describe the cluster centroids, and which cluster each sample is in"""
    kmeans = KMeans(n_clusters=num_clusters).fit(dataset)
    return kmeans

def calculate_composition(km, num_clusters, data_objects):
    """This functoin accepts a kmeans object, a number of clusters and a list of data objects and calculates the composition of each cluster, 
    it returns a pandas dataframe with the composition of each cluster.  Composition dataframe is of shape clusters x categories.
    Each row is a cluster, and each column is a category"""
    comp = pd.DataFrame(index = range(num_clusters))
    for i in range(len(data_objects)):
        category = data_objects[i].descriptive.loc[data_objects[i].descriptive['descriptor'] == 'Type', 'value'][1]
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[km.labels_[i],category] = 1
        else:
            comp.at[km.labels_[i],category] += 1

    return comp