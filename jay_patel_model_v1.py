# -*- coding: utf-8 -*-
"""Jay_Lab2_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OSBQvMPW9pJ6OqnJybb9vkEWZIq5zJTh

1. Import libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""2. Read data"""

df=pd.read_csv('./data.csv')

df.transpose()
df = df.drop(["id", "Unnamed: 32"], axis = 1)
df

"""3. Analysing and Visualising data"""

df.info()

df.describe()

df.describe().transpose()

# matrix of correlation
df.corr()

# figure size
plt.figure(figsize=(20,12))
# correlation matrix
corr = df.corr()
# upper triangle is marked
marked_matrix = np.triu(corr)
# plot heatmap
sns.heatmap(data = corr, cmap='viridis', annot=True, mask = marked_matrix)  #

"""4. Preprocessing data"""

# correlation matrix
corr = df.corr()
corr_abs = corr.abs()
# select upper triangle of correlation matrix
upper_triangle = corr_abs.where(np.triu(np.ones(corr_abs.shape), k=1).astype(np.bool))

# columns with high correlation to be dropped
# dropped_columns = [col for col in upper_triangle.columns if any(upper_triangle[col] > 0.75)]  # this give accuracy 95%
# dropped_columns = [col for col in upper_triangle.columns if any(upper_triangle[col] > 0.8)]     # this give accuracy 95%
dropped_columns = [col for col in upper_triangle.columns if any(upper_triangle[col] > 0.85)]  # accuracy 97%
# dropped_columns = [col for col in upper_triangle.columns if any(upper_triangle[col] > 0.9)]     # 97%

# drop columns from dataframe
df = df.drop(dropped_columns, axis = 1)
df

dropped_columns

len(dropped_columns)

# Features
X = df.drop("diagnosis", axis = 1)

# Target
y = df["diagnosis"]

y.unique()

# figure size
plt.figure(figsize=(8, 5))
sns.countplot(y)

"""5. Spliting and Scaling data"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# We use 30% of data for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# Create an object of StandardScaler
scaler = StandardScaler()

# We only fit to the training data, not test data.
scaled_X_train = scaler.fit_transform(X_train)

# We transform but not fit the test data.
scaled_X_test = scaler.transform(X_test)

"""6. Building the model: Logistic Regression Model"""

from sklearn.linear_model import LogisticRegression

log_model = LogisticRegression()

log_model.fit(scaled_X_train,y_train)

y_pred = log_model.predict(scaled_X_test)
y_pred

"""7. Evaluating model performance"""

from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,plot_confusion_matrix

score = accuracy_score(y_test,y_pred, normalize=True)
score

conf_matrix = confusion_matrix(y_test, y_pred)
conf_matrix

plot_confusion_matrix(log_model,scaled_X_test,y_test)
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 10);

plot_confusion_matrix(log_model,scaled_X_test,y_test,normalize='true')

print(classification_report(y_test,y_pred))

"""8. Plotting performance curves"""

from sklearn.metrics import plot_precision_recall_curve,plot_roc_curve

plot_precision_recall_curve(log_model,scaled_X_test,y_test)

plot_roc_curve(log_model,scaled_X_test,y_test)