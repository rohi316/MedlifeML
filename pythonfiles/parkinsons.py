# -*- coding: utf-8 -*-
"""parkinsons.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RK0qb6WFf-j_xfKFqq9dXzQdgrGzXHnH
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score

# Loading the data from CSV file to a Pandas DataFrame
parkinsons_data = pd.read_csv ("/content/ParkinsonsDisease.csv")

# Exploring Dataset Content
parkinsons_data.head()

# Dropping The Redundant Name Column
parkinsons_data.drop(['name'], axis=1, inplace=True)

# Exploring Information About Dataframe
parkinsons_data.info()

parkinsons_data.describe()

print('Number of Duplicated Rows :',parkinsons_data.duplicated().sum())

parkinsons_data.isnull().sum()

# Exploring Imbalance In Dataset

parkinsons_data['status'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt



sns.countplot(x='status',data=parkinsons_data)

sns.scatterplot(x='MDVP:Jitter(%)',y='MDVP:Jitter(Abs)',data=parkinsons_data,hue='status')
plt.show()

fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(parkinsons_data.corr(),annot=True,ax=ax)

sns.pairplot(parkinsons_data,hue = 'status', vars = ['MDVP:Jitter(%)','MDVP:Jitter(Abs)','MDVP:RAP','MDVP:PPQ', 'Jitter:DDP'] )
plt.show()

sns.pairplot(parkinsons_data,hue = 'status', vars = ['MDVP:Shimmer','MDVP:Shimmer(dB)','Shimmer:APQ3','Shimmer:APQ5','MDVP:APQ','Shimmer:DDA'] )
plt.show()

plt.figure(figsize=(10,8))
selected_columns = ['MDVP:Jitter(%)','MDVP:Jitter(Abs)','MDVP:RAP','MDVP:PPQ', 'Jitter:DDP']

sns.boxplot(data=parkinsons_data[selected_columns])
plt.show()

# Exploring Imabalance In Dataset
parkinsons_data['status'].value_counts()

# Extracting Features Into Features & Target
X = parkinsons_data.drop(['status'], axis=1)
Y = parkinsons_data['status']

print('Feature (X) Shape Before Balancing :', X.shape)
print('Target (Y) Shape Before Balancing :', Y.shape)

from imblearn.over_sampling import SMOTE


# Intialising SMOTE Object
sm = SMOTE(random_state=300)
# Resampling Data
X, Y = sm.fit_resample(X, Y)


print('Feature (X) Shape After Balancing :', X.shape)
print('Target (Y) Shape After Balancing :', Y.shape)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.3,random_state=300)

# Visualising the Original/Train/Test sizes
print ( X.shape,X_train.shape,X_test.shape)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

from sklearn import metrics
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train, Y_train)
Y_pred = lr.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
lr.score(X_train,Y_train)*100,lr.score(X_test,Y_test)*100

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

# Define the hyperparameter configuration space
logreg_params = {
      'penalty': ['l1','l2'],
       'C': [0.01, 0.1, 1, 10],
       'solver': ['liblinear'],
       'max_iter': [100, 200, 500],
          }
# Grid search with 3-fold cross-validation
lr_grid = GridSearchCV(lr, logreg_params, cv=3)
lr_grid.fit(X_train, Y_train)

# Best hyperparameters
print("Best Parameters:", lr_grid.best_params_)
print( lr_grid.best_estimator_)

lr_grid.fit(X_train,Y_train)
Y_pred = lr_grid.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
lr_grid.score(X_train,Y_train)*100,lr_grid.score(X_test,Y_test)*100

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, Y_train)
Y_pred = gnb.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
gnb.score(X_train,Y_train)*100,gnb.score(X_test,Y_test)*100

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

# Define the parameter grid
gnb_params = {
    'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
    }

# Instantiate the model
gnb = GaussianNB()

# Apply GridSearchCV
gnb_grid = GridSearchCV(gnb, gnb_params, cv=3)
gnb_grid.fit(X_train, Y_train)

# Output the best hyperparameters and estimator
print("Best Parameters:", gnb_grid.best_params_)
print("Best Estimator:", gnb_grid.best_estimator_)

gnb_grid.fit(X_train,Y_train)
Y_pred = gnb_grid.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
gnb_grid.score(X_train,Y_train)*100,gnb_grid.score(X_test,Y_test)*100

from sklearn import svm
svm = svm.SVC(kernel='linear')
svm.fit(X_train, Y_train)
Y_pred = svm.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
svm.score(X_train,Y_train)*100,svm.score(X_test,Y_test)*100

#SVM
from sklearn.model_selection import GridSearchCV
svm_params = {
    'C': [1,10, 100],
    "kernel":['linear','sigmoid'],

        }
# Grid search with 3-fold cross-validation
svm_grid = GridSearchCV(svm, svm_params, cv=4)

# Fit the model on training data
svm_grid.fit(X_train, Y_train)

# Best hyperparameters
print("Best Parameters:", svm_grid.best_params_)
print( svm_grid.best_estimator_)

svm_grid.fit(X_train,Y_train)
Y_pred = svm_grid.predict(X_test)
confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
print("-"*70)
print("Report")
print("-"*70)
print("Confusion Matrix:")
print(str(confusion_matrix))
target_names = ['without parkinsons', 'with parkinsons']
acc=(confusion_matrix[0][0] + confusion_matrix[1][1])/(confusion_matrix[0][0]+confusion_matrix[0][1]+confusion_matrix[1][0]+confusion_matrix[1][1])
print("Accuracy by confusion matrix: "+str(acc))
print("\n")
print(classification_report(Y_test, Y_pred, target_names=target_names))
print("-"*70)
svm_grid.score(X_train,Y_train)*100,svm_grid.score(X_test,Y_test)*100

#Building a predictive system
#Data of a parkinson's Disease patient
input_data = (116.68200,131.11100,111.55500,0.01050,0.00009,0.00544,0.00781,0.01633,0.05233,0.48200,0.02757,0.03858,0.03590,0.08270,0.01309,20.65100,0.429895,0.825288,-4.443179,0.311173,2.342259,0.332634)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the input data
std_data = scaler.transform(input_data_reshaped)
print(std_data)

prediction = svm_grid.predict(std_data)
print(prediction)

if (prediction[0] == 0):
  print('The person does not have parkinsons')
else:
  print('The person have parkinsons')

import pickle
# Save the trained SVM model with pickle
pickle.dump(svm_grid, open('parkinsons.pkl', 'wb'))