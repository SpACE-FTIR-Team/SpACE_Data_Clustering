import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


def plot(dataset, clusters):
    x = []
    y = []
    z = []
    cx = []
    cy = []
    for i in dataset[0]:
        x.append(i)
    for i in dataset[1]:
        y.append(i)
    # if z axis is not empty, append to z
    if 2 in dataset.columns:
        for i in dataset[2]:
            z.append(i)
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
    plt.scatter(x= x, y= y, c=clusters.labels_, cmap = "tab20")
    plt.scatter(x = cx, y = cy, marker = "x", color = "black", s = 50)
    plt.title("Kmeans")
    plt.show()
