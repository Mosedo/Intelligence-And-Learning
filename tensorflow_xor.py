from statistics import mode
import tensorflow as tf
from tensorflow import keras
import numpy as np
import math
import random
from keras.layers import Dense,Flatten
from keras.activations import relu,softmax

X=np.array(
    [
        [1,0],
        [1,1],
        [0,1],
        [0,0],
    ]
)

print(X[0].shape)

Y=np.array([
    [1,0],
    [0,1],
    [1,0],
    [0,1],
])


model=keras.Sequential()
model.add(Flatten(input_shape=(2,)))
model.add(Dense(120,activation=relu))
model.add(Dense(2,activation=softmax))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X,Y,epochs=150)

for i in range(0,4):
    print(model.predict(np.array([X[i]])))

# for prediction in model.predict(X):
#     if prediction[0] >= 0.5:
#         print(1)
#     else:
#         print(0)

# print(np.argmin(model.predict(X),axis=1))
# print(model.predict(X[1]))
# print(model.predict(X[2]))
# print(model.predict(X[3]))