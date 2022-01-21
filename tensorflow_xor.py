from statistics import mode
import tensorflow as tf
from tensorflow import keras
import numpy as np
import math
import random
from keras.layers import Dense,Flatten
from keras.activations import relu,softmax
from keras.models import Sequential

X=np.array(
    [
        [1,0],
        [1,1],
        [0,1],
        [0,0],
    ]
)


Y=np.array([
    [1,0],
    [0,1],
    [1,0],
    [0,1],
])


model=Sequential()
model.add(Flatten(input_shape=(2,)))
model.add(Dense(150,activation=relu))
model.add(Dense(2,activation=softmax))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X,Y,epochs=150)

print(model.predict(X))


# for i in range(0,4):
#     print(model.predict(np.array([X[i]])))


# print(np.argmin(model.predict(X),axis=1))
# print(model.predict(X[1]))
# print(model.predict(X[2]))
# print(model.predict(X[3]))