# Normalization functions for SpACE
# Currently includes PCA and linear normalization (0 to 1)

import pandas as pd
import space_preprocess_test
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def PCAnormalize(dataObjectArray, dimensions):
    dataOb = dataObjectArray
    dims = dimensions

    for i in dataOb:
        pca = PCA(n_components=dims, copy=False, svd_solver='full')
        pca.fit(i.pairs)
    # print("PCA done")


def linear_normalize(dataObjectArray):
    """This function normalizes each individual DataFrame's values to range 0 to 1
    Takes the dataObjectArray as a parameter."""
    scaler = preprocessing.MinMaxScaler()
    for i in dataObjectArray:
        normalized_pairs = scaler.fit_transform(i.pairs)
        n = i.pairs.columns[0]
        i.pairs.drop(n, axis=1, inplace=True)
        i.pairs[n] = normalized_pairs
    return dataObjectArray
