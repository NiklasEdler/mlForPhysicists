# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Introduction to TensorFlow and Keras
#
# In this notebook we define a simple network architechture for taking in 1D input. Here we are going to train a network to mimic the behaviour of an arbitrary function.
#
# Once more this notebook is heavily inspired by https://machine-learning-for-physicists.org and is relased under the same Creative Commons License.
#

# +
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
from tensorflow import keras


import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense


#Set default figure size
#mpl.rcParams['figure.figsize'] = [12.0, 8.0] #Inches... of course it is inches
mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch
# -

# ### Define our network
# We will define a network with one input and one output and two hidden layers.
# - First hidden layer has 1 input and 20 neurons with sigmoid activation functions
# - Second hidden layer takes 20 inputs (from the first hidden layer) and has 10 neurons with sigmoid activation functions.
# - Output layer is a single neuron with linear activation function.

model = keras.Sequential([
    keras.layers.Dense(20,input_shape=(1,),activation="sigmoid"),
    keras.layers.Dense(10,activation='sigmoid'),
    keras.layers.Dense(1,activation='linear')
])

# Having defined our network the next step is to compile it, specifing which loss function and which optimiser we want to use. Here we will use the 'adam' optimiser which is adaptive and much more perfromant than the standard gradient descent algorithm.

model.compile(loss='mean_squared_error',optimizer='adam')


# Now lets define our target function

#A wave packet target function
def target_func(y):
    return( np.sin(y)/(1+y**2) ) # a wave packet...


# Rather than using `model.fit` we will use `model.train_on_batch` to illustrate the steps in running the training. Repeatedly running the cell below will have the same effect as increasing the number of batches used in the training.

# +

nbatch = 2000  #Number of batches
batchsize = 100 #Samples per batch
costs=np.zeros(nbatch) #Output array for the costs

#Loop over the batches, get batchsize samples and train the network
for i in range(nbatch):
    x=np.random.uniform(low=-10.0,high=+10.0,size=[batchsize,1]) #Generate batchsize random numbers
    y=target_func(x) #Evaluate the function for each random number
    costs[i]=model.train_on_batch(x,y)  #Train the model on this batch of data
                        
# -

#Here we plot the cost vs batch number 
fig, ax = plt.subplots()  #I like to make plots using this silly fig,ax method but plot how you like
step=np.arange(nbatch)  
ax.plot(step,costs,linewidth=3)
ax.set_xlabel("Batch Number")
ax.set_ylabel("Cost")

# +
# get the output on a 1D grid of points:
N=400 # number of points
y_in=np.zeros([N,1]) # prepare correct shape for network, here N becomes the batch size
y_in[:,0]=np.linspace(-20.0,20.0,N) # fill with interval
y_out=model.predict_on_batch(y_in) # apply the network to this set of points!

# plot it!
fig, ax = plt.subplots() 
ax.plot(y_in,y_out,label="NN")
ax.plot(y_in,target_func(y_in),color="orange",label="true")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
# -

# ## Further work
#
# ### Exercise 1: Make a better network?
# Can you improve the network model and make a better fit to the inpout function? You could try changing the number of neurons per layer, the number of layers, or the activation functions for each layer. What metric would you use for determining if the network was better?
#
# ### Exercise 2: Try other functions
# Are some functions easier to model than others? What types of functions are the most difficult to model?


