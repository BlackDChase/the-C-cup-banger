import pandas as pd
import numpy as np
import csv
import random
from sklearn import preprocessing
from sklearn.cluster import DBSCAN


def gen_data(verbose=False, maxpts=1000):
    """
    Extracts data from the from the file into numpy arrays
    """
    with open('CC GENERAL.csv') as fl:
        XY = csv.reader(fl, delimiter=',')
        X, headers, cust = [], None, []
        for row in XY:
            if not headers:
                headers = row
                continue
            try:
                X.append([float(i) for i in row[1:]])
                cust.append(row[0])
            except:
                if verbose:
                    print("skipping", row, ": bad/missing Input")
            maxpts -= 1
            if maxpts == 0:
                break
        return np.array(X), cust


def get_neighbourhood(p, X, epsilon):
    """
    Returns the epsilon neighbourhood for point p in X
    """
    N = []
    p = np.array(list(p))
    for pp in X:
        if np.linalg.norm(pp-p) <= epsilon:
            N.append(tuple(pp))
    print("Neighbourhood of", p, ": ", N, end="\n")
    return N


def dbscan_clusters(epsilon, minpts, X):
    """
    Execute the DBSCAN algorithm  to form clusters. 
    :epsiolon       The neighbourhood radius for a point
    :minpts         The minimum points required for cluster
                    formation 
    """
    label = {tuple(x): None for x in X}
    clusters = []
    noise = []
    iter = 0
    C = 0
    for p in X:
        p = tuple(p)
        if label[p] != None:
            continue
        print("Now considering point", p)
        N = get_neighbourhood(p, X, epsilon)
        if len(N) < minpts:
            print("Since neighbourhood is less than minpts, classified as noise")
            noise.append(p)
            label[p] = -1
            continue
        C = C + 1
        label[p] = C
        print("Since length of neighbourhood is greater than minpts, we explore the point's unvisited neighbours")
        clusters.append([p])
        for q in N:
            if label[q] == -1:
                label[q] = C
                clusters[-1].append(q)
                print("The point", q,
                      "earlier defined as noise is assigned to cluster", C)
                noise.remove(q)
            if label[q] != None:
                continue
            print("Looking at point", q, "in neighbourhood of", p)
            label[q] = C
            NN = get_neighbourhood(q, X, epsilon)
            if len(NN) >= minpts:
                print("Since neighbourhood of", q,
                      "has more than minpts adding those to the list to explore, also adding", q, "to current cluster")
                N.extend(NN)
            else:
                print("Since neighbourhood of", q,
                      "has less than minpts ignoring those and adding", q, "to current cluster")
            clusters[-1].append(q)
        print()
    print()
    return clusters, label, noise


maxpts = int(
    input('Enter the number of points to be considered from the dataset: '))
X, cust = gen_data(maxpts=maxpts)
# scaler = preprocessing.StandardScaler().fit(X_unscaled)
# X = scaler.transform(X_unscaled)
mapping = {tuple(X[i]): cust[i] for i in range(0, len(X))}
epsilon = float(input("Enter epsilon to consider: "))
minpts = float(input("Enter minpts for neighbourhood: "))
clustering = DBSCAN(eps=3, min_samples=3).fit(X)
print("Official cluster labels from sklearn\n", clustering.labels_)
print("\n------------------------------------------------------------\n")
clusters, label, noise = dbscan_clusters(epsilon, minpts, X)
print("Generated cluster labels\n", label)
print("\n------------------------------------------------------------\n")
cluster_cust = []
for cluster in clusters:
    cluster_cust.append([mapping[x] for x in cluster])
for i in range(0, len(clusters)):
    print("Cluster", i)
    print(cluster_cust[i])
    print()
print("Noise")
print(noise)
