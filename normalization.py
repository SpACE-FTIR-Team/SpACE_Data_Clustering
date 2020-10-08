##Insert standardized heading here

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
    #print("PCA done")
