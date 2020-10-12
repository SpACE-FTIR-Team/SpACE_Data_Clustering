# -*- coding: utf-8 -*-
"""
This is a temporary kmeans clustering file
"""

from sklearn.cluster import KMeans


def do_Kmeans(num_clusters, dataset):
    kmeans = KMeans(n_clusters=num_clusters).fit(dataset)
    return kmeans
