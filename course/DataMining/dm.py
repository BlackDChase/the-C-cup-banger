"""
Data Mining Matmatical Problem Solver
- C1
    - Decision Tree
    - Apriori Algorithm
    - Binning
    - Normalisation
    - Frequent Pattern Growth Tree
    - Chi Square Test
"""

# Imports Libraries
import math
import pandas as pd
import numpy as np
from collections import deque
import sys

# From Libraries
"""
Here Class/methods made using libarary functions
"""

# From Scratch
"""
Here Class/methods made from scratch
"""
class Node:
    def __init__(self):
        self.value = None
        self.child = None
        self.next = None

class DecisionTree:
    """Decision Tree Classifier"""
    def __init__(self,data,target):
        """
        Parameters
        __________
        :param data: dict, feature and label mapped to values for all instance
        Example:
        data={
            "Outlook"   :   ["Sunny","Sunny","Overcast","Rain","Rain"],
            "Temp"      :   [79,56,88,78,66],
            "Target"    :   ["No Play","Play","No Play","No Play","Play"],
        }
        __________
        :param target= string, key of target label
        #"""
        self.target=target
        self.massageData(data)
        pass

    def massageData(self,data):
        """
        Converting it into pd and then back for future csv dataset
        Parameters
        Makes x,labels,labelCategories,labelCategoriesCount,feature,featureName
        __________
        :param data: dict, same as init data
        __________
        :return None
        #"""
        self.features={}
        maxNValues=0
        for i in list(data.keys()):
            if maxNValues < len(list(data[i])):
                maxNValues = len(list(data[i]))
            self.features[i] = list(set(data[i]))
        df = pd.DataFrame(columns=data.keys())
        for i in range(maxNValues):
            for k in data.keys():
                try:
                    df.loc[i,k] = data[k][i]
                except:
                    print(k,"'s size is less then max size of ",maxNValues)
        try:
            self.x = np.array(df.drop(self.target,axis=1).copy())
        except KeyError:
            print(self.target,data.keys(),df.columns)
            sys.exit()
        self.labels = np.array(df[self.target].copy())
        self.labelCategories = list(self.features[self.target])
        self.labelCategoriesCount = [list(self.labels).count(x) for x in self.labelCategories]
        self.featureNames = list(set(self.features.keys()).difference([self.target]))
        return

    pass

class ID3(DecisionTree):
    """Decision Tree Classifier using ID3"""

    def __init__(self,data,target):
        DecisionTree.__init__(self,data,target)
        self.node = None
        self.entropy = self._get_entropy([x for x in range(len(self.labels))])
        pass

    def _get_entropy(self, x_ids):
        """Calculates the entropy.
        Parameters
        __________
        :param x_ids: list, List containing the instances ID's
        __________
        :return: entropy: float, Entropy.
        #"""
        # sorted labels by instance id
        labels = [self.labels[i] for i in x_ids]
        # count number of instances of each category
        label_count = [labels.count(x) for x in self.labelCategories]
        # calculate the entropy for each category and sum them
        entropy = sum([-count / len(x_ids) * math.log(count / len(x_ids), 2) if count else 0 for count in label_count])
        return entropy

    def _get_information_gain(self, x_ids, feature_id):
        """Calculates the information gain for a given feature based on its entropy
        and the total entropy of the system.
        Parameters
        __________
        :param x_ids: list, List containing the instances ID's
        :param feature_id: int, feature ID
        __________
        :return: infoGain: float, the information gain for a given feature.
        #"""
        # calculate total entropy
        infoGain = self._get_entropy(x_ids)
        # store in a list all the values of the chosen feature
        xFeat = [self.x[x][feature_id] for x in x_ids]
        # get unique values
        feature_vals = list(set(xFeat))
        # get frequency of each value
        feature_vals_count = [xFeat.count(x) for x in feature_vals]
        # get the feature values ids
        feature_vals_id = [
            [x_ids[i]
            for i, x in enumerate(xFeat)
            if x == y]
            for y in feature_vals
        ]

        # compute the information gain with the chosen feature
        infoGain = infoGain - sum([val_counts / len(x_ids) * self._get_entropy(val_ids)
                                     for val_counts, val_ids in zip(feature_vals_count, feature_vals_id)])

        return infoGain

    def _get_feature_max_information_gain(self, x_ids, feature_ids):
        """Finds the attribute/feature that maximizes the information gain.
        Parameters
        __________
        :param x_ids: list, List containing the samples ID's
        :param feature_ids: list, List containing the feature ID's
        __________
        :returns: string and int, feature and feature id of the feature that maximizes the information gain
        """
        # get the entropy for each feature
        features_entropy = [self._get_information_gain(x_ids, feature_id) for feature_id in feature_ids]
        # find the feature that maximises the information gain
        max_id = feature_ids[features_entropy.index(max(features_entropy))]

        return self.featureNames[max_id], max_id

    def id3(self):
        """Initializes ID3 algorithm to build a Decision Tree Classifier.
        :return: None
        """
        x_ids = [x for x in range(len(self.x))]
        feature_ids = [x for x in range(len(self.featureNames))]
        self.node = self._id3_recv(x_ids, feature_ids, self.node)
        print('')

    def _id3_recv(self, x_ids, feature_ids, node):
        """ID3 algorithm. It is called recursively until some criteria is met.
        Parameters
        __________
        :param x_ids: list, list containing the samples ID's
        :param feature_ids: list, List containing the feature ID's
        :param node: object, An instance of the class Nodes
        __________
        :returns: Instance of the class Node containing all the information of the nodes in the DT
        """
        if not node:
            node = Node()  # initialize nodes
        # sorted labels by instance id
        labels_in_features = [self.labels[x] for x in x_ids]
        # if all the example have the same class (pure node), return node
        if len(set(labels_in_features)) == 1:
            node.value = self.labels[x_ids[0]]
            return node
        # if there are not more feature to compute, return node with the most probable class
        if len(feature_ids) == 0:
            node.value = max(set(labels_in_features), key=labels_in_features.count)  # compute mode
            return node
        # else...
        # choose the feature that maximizes the information gain
        best_feature_name, best_feature_id = self._get_feature_max_information_gain(x_ids, feature_ids)
        node.value = best_feature_name
        node.child = []
        # value of the chosen feature for each instance
        feature_values = list(set([self.x[x][best_feature_id] for x in x_ids]))
        # loop through all the values
        for value in feature_values:
            child = Node()
            child.value = value  # add a branch from the node to each feature value in our feature
            node.child.append(child)  # append new child node to current node
            child_x_ids = [x for x in x_ids if self.x[x][best_feature_id] == value]
            if not child_x_ids:
                child.next = max(set(labels_in_features), key=labels_in_features.count)
                print('')
            else:
                if feature_ids and best_feature_id in feature_ids:
                    to_remove = feature_ids.index(best_feature_id)
                    feature_ids.pop(to_remove)
                # recursively call the algorithm
                child.next = self._id3_recv(child_x_ids, feature_ids, child.next)
        return node

    def printTree(self):
        if not self.node:
            return
        nodes = deque()
        nodes.append(self.node)
        while len(nodes) > 0:
            node = nodes.popleft()
            print(node.value)
            if node.child:
                for child in node.child:
                    print('({})'.format(child.value))
                    nodes.append(child.next)
            elif node.next:
                print(node.next)
    pass
