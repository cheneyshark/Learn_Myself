# coding: utf-8

import pandas as pd
import numpy as np
import random as rd

import seaborn as sns
import matplotlib.pyplot as plt

train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# print train_data[['Pclass','Survived']].groupby(by=['Pclass'],as_index=False).mean().sort_values(by='Survived')
# print train_data[['Sex','Survived']].groupby(['Sex'],as_index=False).mean()




