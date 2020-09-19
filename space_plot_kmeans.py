import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


def plot(dataset, clusters):
    x = []
    y = []
    for i in dataset:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x= x, y= y, c=clusters.labels_, )
    plt.scatter(clusters.cluster_centers_)
    plt.show()