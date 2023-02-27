# -*- coding: utf-8 -*-
"""Prediction of Death Related to Heart Failure

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glpnacisXdJRAv_3Ydf3M8p3rcm4I8-P

**Important Note : To run the code a folder with the name Project is needed with it containing the Kaggle Api Key in Google Drive**

Dataset Url: https://www.kaggle.com/andrewmvd/heart-failure-clinical-data

**Import Data**
"""

import pandas as pd
import numpy as np
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import drive
drive.mount('/content/gdrive')
import os
os.environ['KAGGLE_CONFIG_DIR'] = "/content/gdrive/My Drive/Project"

"""Navigate to Directory With Kaggle Api Key"""

cd /content/gdrive/MyDrive/Project

"""Download Dataset and Unzip"""

!kaggle datasets download -d andrewmvd/heart-failure-clinical-data
!unzip \*.zip  && rm *.zip

"""**Data Preprocessing**"""

data = pd.read_csv('heart_failure_clinical_records_dataset.csv')
data.head()

data.shape

train,validation, test = np.split(data, [int(.8 * len(data)), int(.8 * len(data))])

Y = data.DEATH_EVENT

features = ['age','anaemia', 'diabetes','creatinine_phosphokinase', 'ejection_fraction', 'high_blood_pressure', 'serum_sodium', 'sex', 'smoking', 'time', 'platelets']

X = data[features]
X

"""**Data Normalization**"""

X = (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))
Y = (Y - np.min(Y, axis=0)) / (np.max(Y, axis=0) - np.min(Y, axis=0))

x_train,x_validation, x_test = np.split(X, [int(.8 * len(data)), int(.8 * len(data))])
y_train,y_validation, y_test = np.split(Y, [int(.8 * len(data)), int(.8 * len(data))])

x_train

"""**Build Model**"""

model = models.Sequential([
    layers.Input(shape=(11,)),
    layers.Dense(64, activation='relu', name='Hidden_Layer_1'),
    layers.Dense(32, activation='relu', name='Hidden_Layer_2'),
    layers.Dense(16, activation='relu', name='Hidden_Layer_3'),
    layers.Dense(8, activation='relu', name='Hidden_Layer_4'),
    layers.Dense(1, activation='sigmoid'),
])
model.compile(
    loss = losses.BinaryCrossentropy(),
    optimizer = optimizers.Adam(learning_rate=0.01),
    metrics = ['accuracy']
)

model.summary()

history = model.fit(x_train, y_train, epochs=30, verbose=1)

"""**Test Model Using Test Data**"""

model.evaluate(x_test, y_test)

plt.plot(history.history['accuracy'])
plt.title('Accuracy')
plt.show()

plt.plot(history.history['loss'])
plt.title('Loss')
plt.show()

"""**Comparing Acutal Vs Predicted Death Event**"""

prediction = model.predict(x_test)

mean = max(prediction)/2.0
prediction[prediction >= mean] = 1 
prediction[prediction < mean] = 0

plt.plot(y_test, '.')
plt.title('Actual Death Event')
plt.show()

plt.plot(prediction, '.')
plt.title('Predicted Death Event')
plt.show()

'''
The following heatmap shows the corrrelation between all the variables in our 
dataset with the death event. Time and death even have a negative correlation
which makes sense.  
'''
plt.figure(figsize=(14,4))
data_corr = data.corr()
corr_map = sns.heatmap(data_corr, linewidths=1,cmap= "Reds", annot=True)
corr_map.set_xticklabels(corr_map.get_xticklabels(),rotation = 30, ha='right')
plt.title("Correlation of Health Factors and Death Event Due to Heart Failure")
plt.show()