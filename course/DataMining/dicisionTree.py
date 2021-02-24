"""
Data Mining Matmatical Problem Solver
- Decision Tree
    -ID3
"""

# Imports Libraries
import math
import pandas as pd
import numpy as np
from collections import deque
import sys, os
import graphviz

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
        self.child = []
        self.parent = None

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
        self.target = target
        self.massageData(data)
        self.tree = graphviz.Digraph()
        pass

    def massageData(self,data):
        """
        Converting it into pd and then back for future csv dataset
        Parameters
        Makes x,labels,labelCategories,labelCategoriesCount,feature,featureNames
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
        self.df = df
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
        self.getEntropy()
        pass

    def getEntropy(self,df,featureNames):
        entropy={}
        for f in featureNames:
            entropy[f] = 0
            for vals in self.features[f]:
                pX = sum(df[f]==vals)/len(df[f])
                entropy[f] -= pX*math.log2(pX)
        for k in entropy.keys():
            print(k,":",entropy[k])
        return entropy

    def informationGain(self,df,featureNames,entropy):
        
    def start(self):
    pass

data={
    "Outlook"   :   ["Sunny","Sunny","Overcast","Rain","Rain"],
    "Temp"      :   [79,56,88,78,66],
    "Target"    :   ["No Play","Play","No Play","No Play","Play"],
}
ID3(data,"Target")
