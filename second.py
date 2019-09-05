
import random

import numpy

import classes.Firing_List as FL
import classes.Neuron as N

import classes.Neuron_Network as NN 
import classes.Grid as G



#notes
#threshold is being stored multiple times although it doesnt change
#sensitiviy is not dynamic

test = NN.Neuron_Network()
#I REMOVED PRINTING FROM INITILIZATION
neurons = test.complex_light_setup(3,3,3,10)

map = G.Grid(2,2)

grid_x = 2
grid_y = 2
grid_options = 3 #goal, empty, flint
inputs = grid_x*grid_y*grid_options


iterations = 50
cycles = 100000

#throw in some negatives in creation

for i in range(cycles):
  rewards=[0]
  for i in range(iterations):
    test.pulse([neurons[0][0]],[1],rewards)
    test.count += 1

  rewards[0]= 1
  for i in range(iterations):
    test.pulse([neurons[0][1]],[1],rewards)
    test.count += 1

  rewards[0]= 2
  for i in range(iterations):
    test.pulse([neurons[0][2]],[1],rewards)
    test.count += 1


print test.pulse([neurons[0][0]],[1],rewards)
rewards[0]= 1
print test.pulse([neurons[0][1]],[1],rewards)
rewards[0]= 2
print test.pulse([neurons[0][2]],[1],rewards)