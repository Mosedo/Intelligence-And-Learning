import numpy as np
import math
import random

weights_ihidd=np.array([[ 0.22879112],
                        [ 1.83236638],
                        [ 0.26723785],
                        [ 0.03798854],
                        [-1.0188697 ]])

weights_hout=np.array([[ 0.26961465,  0.77256597, -0.11073264, -1.2405121,   0.2969469 ]])
class Brain:
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.input_nodes=input_nodes
        self.hidden_nodes=hidden_nodes
        self.output_nodes=output_nodes
        self.weights_ih=weights_ihidd
        self.weights_ho=weights_hout
        self.fitness=0

    def feedFoward(self,inputs):
        input_hidden=np.dot(self.weights_ih,np.array(inputs))
        output=np.dot(self.weights_ho,input_hidden)
        return output

nn=Brain(1,10,1)

while True:
    x=int(input("Enter x value: "))
    print(nn.feedFoward([x/900]))


