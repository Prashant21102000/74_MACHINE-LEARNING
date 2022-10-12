# -*- coding: utf-8 -*-
"""mlexp4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j1NFzbhyh-b0T9OFv6bm16R1Uzz1X4lS
"""

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

from google.colab import files
 
 
uploaded = files.upload()

dataset = pd.read_csv('adult.csv')

# Check for null values
round((dataset.isnull().sum() / dataset.shape[0]) * 100, 2).astype(str) + ' %'

dataset = dataset.replace('?', np.nan)

round((dataset.isnull().sum() / dataset.shape[0]) * 100, 2).astype(str) + ' %'

columns_with_nan = ['workclass', 'occupation', 'native.country']
for col in columns_with_nan:
    dataset[col].fillna(dataset[col].mode()[0], inplace=True)

from sklearn.preprocessing import LabelEncoder

for col in dataset.columns:
    if dataset[col].dtypes == 'object':
        encoder = LabelEncoder()
        dataset[col] = encoder.fit_transform(dataset[col])

X = dataset.drop('income', axis=1)
Y = dataset['income']

from sklearn.ensemble import ExtraTreesClassifier
selector = ExtraTreesClassifier(random_state=42)
selector.fit(X, Y)

feature_imp = selector.feature_importances_
for index, val in enumerate(feature_imp):
    print(index, round((val * 100), 2))

X = X.drop(['workclass', 'education', 'race', 'sex',
            'capital.loss', 'native.country'], axis=1)

from sklearn.preprocessing import StandardScaler
for col in X.columns:
    scaler = StandardScaler()
    X[col] = scaler.fit_transform(X[col].values.reshape(-1, 1))
round(Y.value_counts(normalize=True) * 100, 2).astype('str') + ' %'

from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=42)
ros.fit(X, Y)
X_resampled, Y_resampled = ros.fit_resample(X, Y)
round(Y_resampled.value_counts(normalize=True) * 100, 2).astype('str') + ' %'

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    X_resampled, Y_resampled, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
ran_for = RandomForestClassifier(random_state = 42)
ran_for.fit(X_train, Y_train)
Y_pred_ran_for = ran_for.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

print('Random Forest Classifier:')
print('Accuracy score:',round(accuracy_score(Y_test, Y_pred_ran_for) * 100, 2))
print('F1 score:',round(f1_score(Y_test, Y_pred_ran_for) * 100, 2))

from sklearn.model_selection import RandomizedSearchCV
n_estimators = [int(x) for x in np.linspace(start = 40, stop = 150, num = 15)]
max_depth = [int(x) for x in np.linspace(40, 150, num = 15)]
param_dist = {
    'n_estimators' : n_estimators,
    'max_depth' : max_depth,
}
rf_tuned = RandomForestClassifier(random_state = 42)
rf_cv = RandomizedSearchCV(estimator = rf_tuned, param_distributions = param_dist, cv = 5, random_state = 42)

rf_best = RandomForestClassifier(max_depth = 102, n_estimators = 40, random_state = 42)
rf_best.fit(X_train, Y_train)
Y_pred_rf_best = rf_best.predict(X_test)
print('Random Forest Classifier:') 
print('Accuracy score:',round(accuracy_score(Y_test, Y_pred_rf_best) * 100, 2)) 
print('F1 score:',round(f1_score(Y_test, Y_pred_rf_best) * 100, 2))

from sklearn.metrics import confusion_matrix 
cm = confusion_matrix(Y_test, Y_pred_rf_best)
cm

from sklearn.metrics import classification_report
print(classification_report(Y_test, Y_pred_rf_best))