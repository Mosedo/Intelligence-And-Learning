import numpy as np
import math
import random

from numpy.core.fromnumeric import size


class Brain:
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.input_nodes=input_nodes
        self.hidden_nodes=hidden_nodes
        self.output_nodes=output_nodes
        self.wh=np.random.uniform(-2,2,size=(self.hidden_nodes,self.input_nodes))
        self.wout=np.random.uniform(-2,2,size=(self.output_nodes,self.hidden_nodes))
        self.bh=np.array([1])
        self.bout=np.array([1])
    def feedFoward(self,input):
        hidden_inputs=np.dot(self.wh,input)
        hidden_inputs=hidden_inputs+self.bh
        hidden_inputs=np.tanh(hidden_inputs)
        output=np.dot(self.wout,hidden_inputs)
        output=output+self.bout
        output=np.tanh(output)
        return output
    
    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    

# nn=Brain(4,4,1)

# print(nn.feedFoward([100/500,200/500,300/500,400/500])[0])