# Normalization functions for SpACE
# Currently includes PCA and linear normalization (0 to 1)

import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA


def linear_normalize(dataObjectArray):
    scaler = preprocessing.MinMaxScaler()
    for i in dataObjectArray:
        normalized_pairs = scaler.fit_transform(i.pairs)
        n = i.pairs.columns[0]
        i.pairs.drop(n, axis=1, inplace=True)
        i.pairs[n] = normalized_pairs
    return dataObjectArray


def PCAnormalize(dataObjectArray, dimensions):
    pca = PCA(n_components=dimensions, copy=False, svd_solver='full')
    pca.fit(dataObjectArray)
    transformed = pca.transform(dataObjectArray)
    return transformed
