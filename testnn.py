import numpy as np
import math
import random

weights_ihidd=np.array([[2.37004549, 4.94034828],
                        [2.38451919, 5.04085224]])

weights_hout=np.array([[-5.34496779],
                        [ 5.35608423]])

bias_hidden=np.array([[-3.50020761, -1.62119614]])

bias_out=np.array([[-2.40216604]])
class Brain:
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.lr=0.1
        self.fitness=0
        self.input_nodes = input_nodes 
        self.hidden_nodes = hidden_nodes
        self.output_nodes= output_nodes 

        # initializing weight and bias
        self.wh=weights_ihidd
        self.bh=bias_hidden
        self.wout=weights_hout
        self.bout=bias_out

    def feedFoward(self,inputs):
        hidden_layer_input1=np.dot(np.array([[inputs]]),self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        output = self.sigmoid(output_layer_input)

        return output
    
    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    
    def addBias(self,input,bias):
        res=np.add(input,bias)
        return res

    def activation(self,input):
        activate_lambda=lambda n:self.sigmoid(n)
        r=map(activate_lambda,input)
        return np.array(list(r))
    
    def dsigmoid(self,x):
        #return self.sigmoid(x)*(1-self.sigmoid(x))
        return x*(x-1)
    
    def derivative(self,input):
        der_lambda=lambda n:self.dsigmoid(n)
        r=map(der_lambda,input)
        return np.array(list(r))
    
    def derivatives_sigmoid(self,x):
        return x * (1 - x)

nn=Brain(2,2,1)

print("***************************************")
print(nn.feedFoward([1,0]))
print(nn.feedFoward([0,0]))
print(nn.feedFoward([0,1]))
print(nn.feedFoward([1,1]))


