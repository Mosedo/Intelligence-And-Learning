import numpy as np
from numpy import random
import math

X=np.array([[1,0],[0,1],[1,1],[0,0]])

y=np.array([[1],[1],[0],[0]])





class NeuralNetwork:

    def __init__(self,hidden_nodes,output_nodes):

        self.lr=0.1
        self.input_nodes = X.shape[1] # number of features in data set
        self.hidden_nodes = hidden_nodes # number of hidden layers neurons
        self.output_nodes= output_nodes # number of neurons at output layer

        # initializing weight and bias
        self.wh=np.random.uniform(size=(self.input_nodes,self.hidden_nodes))
        self.bh=np.random.uniform(size=(1,self.hidden_nodes))
        self.wout=np.random.uniform(size=(self.hidden_nodes,self.output_nodes))
        self.bout=np.random.uniform(size=(1,self.output_nodes))


    def feedFoward(self,X):
        #Forward Propogation
        hidden_layer_input1=np.dot(np.array([[X]]),self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        output = self.sigmoid(output_layer_input)

        return output
    
    def train(self,X,y):
        #Forward Propogation
        hidden_layer_input1=np.dot(X,self.wh)
        hidden_layer_input=hidden_layer_input1 + self.bh
        hiddenlayer_activations = self.sigmoid(hidden_layer_input)
        output_layer_input1=np.dot(hiddenlayer_activations,self.wout)
        output_layer_input= output_layer_input1+ self.bout

        output = self.sigmoid(output_layer_input)

        #Backpropagation
        E = y-output
        #print(f"Error is {E}")
        slope_output_layer = self.derivatives_sigmoid(output)
        slope_hidden_layer = self.derivatives_sigmoid(hiddenlayer_activations)
        d_output = E * slope_output_layer
        Error_at_hidden_layer = d_output.dot(self.wout.T)
        d_hiddenlayer = Error_at_hidden_layer * slope_hidden_layer
        self.wout += hiddenlayer_activations.T.dot(d_output) *self.lr
        self.bout += np.sum(d_output, axis=0,keepdims=True) *self.lr
        self.wh += X.T.dot(d_hiddenlayer) *self.lr
        self.bh += np.sum(d_hiddenlayer, axis=0,keepdims=True) *self.lr


        print((self.wh,self.wout,self.bh,self.bout))

        return E

    
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


        

nn=NeuralNetwork(2,1)


#print(nn.feedFoward([1,0]))

# print(nn.train([0.8,0.6],[1]))

for i in range(5000):
    #print(nn.train(X,y))
    nn.train(X,y)

print("***************************************")
print(nn.feedFoward([1,0]))
print(nn.feedFoward([0,0]))
print(nn.feedFoward([0,1]))
print(nn.feedFoward([1,1]))

# print(nn.feedFoward([0.5]))
# print(nn.feedFoward([0.1]))
# print(nn.feedFoward([0.6]))
# print(nn.feedFoward([0.8]))
