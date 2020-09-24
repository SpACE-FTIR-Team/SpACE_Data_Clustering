import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


def plot(dataset, clusters):
    x = []
    y = []
    cx = []
    cy = []
    for i in dataset:
        x.append(i[0])
        y.append(i[1])
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
    plt.scatter(x= x, y= y, c=clusters.labels_, cmap = "Dark2")
    plt.scatter(x = cx, y = cy, marker = "x", color = "black", s = 50)
    plt.show()