import numpy as np
import math
import random


X=np.array([[1,0],[0,1],[1,1],[0,0]])

y=np.array([[1],[1],[0],[0]])



class Brain:
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.lr=0.1
        self.fitness=0
        self.input_nodes = input_nodes 
        self.hidden_nodes = hidden_nodes
        self.output_nodes= output_nodes 

        # initializing weight and bias
        self.wh=np.array([np.random.uniform(-2,1) for i in range((self.input_nodes*self.hidden_nodes))]).reshape(self.input_nodes,self.hidden_nodes)
        self.bh=np.random.uniform(size=(1,self.hidden_nodes))
        self.wout=np.array([np.random.uniform(-2,1) for i in range((self.output_nodes*self.hidden_nodes))]).reshape(self.hidden_nodes,self.output_nodes)
        self.bout=np.random.uniform(size=(1,self.output_nodes))

    def feedFoward(self,inputs):
        hidden_layer_input1=np.dot(np.array([[inputs]]),self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        #output = self.sigmoid(output_layer_input)

        output=np.tanh(output_layer_input)

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
    
    def mutate(self):
        mutation_value=np.random.uniform(-1,1)
        self.wh+=mutation_value
        self.wout+=mutation_value
        self.bh+=mutation_value
        self.bout+=mutation_value
        return self.wh,self.wout,self.bh,self.bout

nn=Brain(2,2,1)

print(nn.feedFoward([1,0]))

