import numpy as np
import math
import random



class Brain:
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.input_nodes=input_nodes
        self.hidden_nodes=hidden_nodes
        self.output_nodes=output_nodes
        self.weights_ih=np.random.normal(size=(self.hidden_nodes,self.input_nodes))
        self.weights_ho=np.random.normal(size=(self.output_nodes,self.hidden_nodes))
        self.fitness=0

    def feedFoward(self,inputs):
        input_hidden=np.dot(self.weights_ih,np.array(inputs))
        output=np.dot(self.weights_ho,input_hidden)
        return output

