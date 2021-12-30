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
        self.wh=np.random.uniform(size=(self.input_nodes,self.hidden_nodes))
        self.bh=np.random.uniform(size=(1,self.hidden_nodes))
        self.wout=np.random.uniform(size=(self.hidden_nodes,self.output_nodes))
        self.bout=np.random.uniform(size=(1,self.output_nodes))

    def feedFoward(self,inputs):
        hidden_layer_input1=np.dot(np.array([[inputs]]),self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        output = self.sigmoid(output_layer_input)

        # return {"output":output,"hidden_activation":hiddenlayer_activations}
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
        
    
    def train(self,input):

        #Forward Propogation
        hidden_layer_input1=np.dot(input,self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        output = self.sigmoid(output_layer_input)
        #Backpropagation
        E = y-output
        slope_output_layer = self.derivatives_sigmoid(output)
        slope_hidden_layer = self.derivatives_sigmoid(hiddenlayer_activations)
        d_output = E * slope_output_layer
        Error_at_hidden_layer = d_output.dot(self.wout.T)
        d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
        self.wout += hiddenlayer_activations.T.dot(d_output) *self.lr
        self.bout += np.sum(d_output, axis=0,keepdims=True) *self.lr
        self.wh += X.T.dot(d_hiddenlayer) *self.lr
        self.bh += np.sum(d_hiddenlayer, axis=0,keepdims=True) *self.lr

        return self.wh,self.wout,self.bh,self.bout

