import imp
import random
import math
import numpy as np
import string
# import tensorflow as tf
# from tensorflow import keras
import warnings



warnings.filterwarnings("ignore")

#tf.config.experimental.list_physical_devices('GPU')

from hmmlearn.hmm import MultinomialHMM
from hmmlearn.hmm import GaussianHMM

start_prob=np.array([0.5,0.5])

tran_mat=np.array([
    [0.7,0.3],
    [0.4,0.6]
])

emmision_matr=[
        [0.1,0.4,0.5],
        [0.6,0.3,0.1]
]

model=MultinomialHMM(n_components=2,startprob_prior=start_prob,transmat_prior=tran_mat)
model.emissionprob_=emmision_matr
#model=GaussianHMM()



X=[
    [1,1,0,0],
    [0,1,1,0],
    [1,1,1,0],
    [0,0,0,0],
    [0,1,0,0]
]
model.fit(X)
prob=model.decode(np.array([1,0,1,0]).reshape(4,1))

print(np.exp(prob[0]))

x, Z = model.sample(100)
print(Z)

#print(model.transmat_)