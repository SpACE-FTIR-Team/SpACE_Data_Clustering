##Insert standardized heading here

import pandas as pd
import space_preprocess_test
import space_data_ops as dataops
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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
