# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:46:22 2019


Load MNIST dataset and implement a deterministic autoencoder with only a few layers to do manifold learning

@author: rvulling
"""

import struct as st
from collections import defaultdict

import numpy as np
import math
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense, Conv2D, LeakyReLU, AvgPool2D, UpSampling2D, ReLU, MaxPooling2D, Reshape, Flatten
from tensorflow.keras.losses import MSE
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam

#from IPython.display import clear_output
import matplotlib.pyplot as plt

import sklearn

from sklearn.datasets import fetch_openml
from sklearn.preprocessing import OneHotEncoder
#%%
epochs = 5
batch_size=10000


def build_batches(x, n):
    m = (x.shape[0] // n) * n
    return x[:m].reshape(-1, n, *x.shape[1:])

def get_mnist32_batches(batch_size, data_format='channels_last'):
    maxNum_data_train=10000 #reduce data size for computational load
    maxNum_data_test=1000
    channel_index = 1 if data_format == 'channels_first' else 3
    mnist = fetch_openml('mnist_784')
    data_x = mnist['data'].reshape(-1,28,28).astype(np.float32) / 255.
    print(data_x.shape)
    #Reduce dimensions of dataset to reduce computations times
    np.random.seed(42) #seed to ensure reproducible results
    randomIndices=np.random.permutation(np.size(data_x,0))
    indicesTrain=randomIndices[0:maxNum_data_train]
    indicesTest=randomIndices[np.size(data_x,0)-maxNum_data_test:np.size(data_x,0)]
    data_x_train=  data_x[indicesTrain,:,:] #Reduce dimensions of dataset to reduce computations times
    data_x_train = np.pad(data_x_train, ((0,0), (2,2), (2,2)), mode='constant')
    data_x_train = np.expand_dims(data_x_train, channel_index)
    data_x_test = data_x[indicesTest,:,:]
    data_x_test = np.pad(data_x_test, ((0,0), (2,2), (2,2)), mode='constant')
    data_x_test = np.expand_dims(data_x_test, channel_index)
    data_y = mnist['target']
    data_y_train=data_y[indicesTrain] #Reduce dimensions of dataset to reduce computations times
    data_y_test=data_y[indicesTest] #Reduce dimensions of dataset to reduce computations times
    indices = np.arange(len(data_x_train))
    #np.random.shuffle(indices)
    y_batches = build_batches(data_y_train[indices], batch_size)
    x_batches = build_batches(data_x_train[indices], batch_size)
    return x_batches, y_batches, data_x_train, data_y_train, data_x_test, data_y_test

x_batches, y_batches, data_x_train, data_y_train, data_x_test, data_y_test = get_mnist32_batches(batch_size)


#%% Model definition
def Encoder(input_shape):
    #ENCODER
    f=Sequential()
    f.add(Conv2D(16, (3, 3), activation='relu', padding='same',input_shape=(input_shape)))
    f.add(MaxPooling2D((2, 2), padding='same'))
    f.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    f.add(MaxPooling2D((2, 2), padding='same'))
    f.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    f.add(MaxPooling2D((2, 2), padding='same'))
    f.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    f.add(MaxPooling2D((2, 2), padding='same'))
    f.add(Flatten())
    f.add(Dense(10,activation = "softmax"))
    
    f.summary()
    """
    Complete this part
    """
    
    return f


input_shape = x_batches.shape[2:]
encoder=Encoder(input_shape)
input_shape_decoder=encoder.output_shape[1:]
input_shape=x_batches.shape[2:]
inputs=Input(input_shape)
encoded=encoder(inputs)



# saver = tf.train.Saver()
# saver.restore(session,"data\\model.ckpt")
y_batches = np.array( [int (item) for item in y_batches[0]])
data_y_test = np.array( [int (item) for item in data_y_test])
y_batches=  tf.keras.utils.to_categorical(y_batches, 10)
data_y_test = tf.keras.utils.to_categorical(data_y_test, 10)
print(data_y_test.shape)
print(data_x_test.shape)
 #OneHotEncoder().fit_transform(y_batches)
model=tf.keras.Model(inputs=inputs,outputs = encoded)
model.compile('adam',loss= "categorical_crossentropy", metrics=["accuracy"])
loss=[]
loss_val=[]
acc=[]
acc_val=[]
for i in range(epochs): 
    batch_idx = random.randint(0,x_batches.shape[0]-1)
    print("Epoch {} out of {}".format(i,epochs))
    
    history=model.fit(x_batches[0], y_batches, validation_data=(data_x_test,data_y_test))
    loss+=[history.history['loss']]
    loss_val+=[history.history['val_loss']] 
    acc+=[history.history['acc']]
    acc_val+=[history.history['val_acc']]    
# saver.save(session,"data\\model.ckpt")    
plt.figure()
plt.plot(loss,label = "train")
plt.plot(loss_val,label = "test")
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend()

plt.figure()
plt.plot(acc,label = 'train')
plt.plot(acc_val,label = "test")
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend()


plt.show()