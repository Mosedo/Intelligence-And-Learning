import numpy as np
import math
import random

weights_ihidd=np.array([[ 0.27641065, -0.12879777],
                        [ 0.11672074,  1.18172682]])

weights_hout=np.array([[ 0.35780877, -0.09109436],
                        [ 1.01166643, -0.54294083]])
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


