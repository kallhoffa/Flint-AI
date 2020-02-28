import random

import numpy

import classes.Firing_List as FL
import classes.Neuron as N

import classes.Neuron_Network as NN 
import classes.Grid as G

import thread
import sys

def input_thread(a_list):
    raw_input()
    a_list.append(True)

def do_stuff():
    a_list = []
    thread.start_new_thread(input_thread, (a_list,))
    while not a_list:
        stuff()


#sends one pulse to the network based on the current configuration of grid.  Then records any movements outputed. Make moves on grid. Returns true if movement results in goal. 
def oneMove(neurons,test,grid):
  activated = []

  i = 0
  for x in range(grid_x):
    for y in range(grid_y):
      if grid.grid[x][y] == 'F':
        activated.append(neurons[0][i]) #the f neuron for this cluster is activated
      elif grid.grid[x][y] == 'G':
        activated.append(neurons[0][i+1]) #the g neuron for this cluster is activated

      i = i + 2 # move to the next neuron cluster

  movements = test.pulse(activated,[1,1],rewards=None) #pulse the neurons that have inputs


  goal = grid.move(movements,False,0)

  return goal

def printMove(neurons,test,grid,pulses):
  activated = []

  i = 0
  for x in range(grid_x):
    for y in range(grid_y):
      if grid.grid[x][y] == 'F':
        activated.append(neurons[0][i])
      elif grid.grid[x][y] == 'G':
        activated.append(neurons[0][i+1])

      i = i + 2

  movements = test.pulse(activated,[1,1],rewards=None)

  goal = grid.move(movements,True,pulses)

  #test.printNetwork()

  return goal

#notes
#threshold is being stored multiple times although it doesnt change
#sensitiviy is not dynamic

# #----------------------------
# #----Configuration------------------
# #--------------------------
# test = NN.Neuron_Network()
#
# best = 15
#
# grid_x = 3
# grid_y = 3
# grid_options = 2 #goal, flint, (empty is granted)
# inputs = grid_x*grid_y*grid_options
# outputs = 4 #up, down, left, right
# iterations = 1000000
# second_iterations = 2000
# file_name = "grid_network_delayed.txt"


grid = G.Grid(grid_x,grid_y)
neurons = test.complex_light_setup(inputs,outputs,3,inputs*3)
#neurons = test.load(file_name)
#neurons = test.load("best.txt")


#grid.print_grid()

#----------------------
#-EXECUTION-------------------
#-----------------------
count = 0  #number of pulses for a grid
solved_boards = 0 #number of solved boards
average_pulses = 50000  #the average pulses for solved boards
good_zone = 0 # the number of solved boards while average below a number
GOAL_PULSES = 5 # to be below to enter good zone
i = 0 #number of boards
save_point = 0 # a tracker for saving
printed = False
bad_count = 0

#create a seperate process to signal when to stop
a_list = [] # needed so that you can press space to stop while running and move on
thread.start_new_thread(input_thread, (a_list,)) #have two threads run
while (good_zone < 100) and (not a_list):

  if oneMove(neurons,test,grid): #when it reaches the goal
    test.d += (1.0-test.d)*0.5 #reward test and start over
    #print("       BREAK          ")
    #test.recently_fired.print_list()
    printed = False
    if solved_boards < 100:
      weight = 50
    else:
      weight = 50
    average_pulses = (average_pulses*weight + count)/(weight + 1.0)
    if average_pulses < GOAL_PULSES:
      good_zone += 1;
    solved_boards += 1
    i+=1
    print i, " average = ", average_pulses, "; This = ", count, "; D = ", float(test.d)
    grid = G.Grid(grid_x,grid_y) #create new grid
  
    count = 0
    bad_count = 0
    #skip = raw_input("Press enter to continue...or enter another key to skip")
    #if skip != "":
    #  break

  else:
    count += 1
    if count == bad_count + 1000:
      bad_count = count
      print "count", count
      test.save("bad.txt",neurons)

    #Debugging
    if (not printed):
      #test.recently_fired.print_list()
      printed = True

  if(average_pulses <= best):
    test.save("best.txt",neurons)
    best = average_pulses - 1.0

  if solved_boards == save_point + 20:
    test.save(file_name, neurons)
    save_point = solved_boards

if not a_list:
  a_list.append(True)

test.save(file_name, neurons)

#new grid created at end of last phase
grid.print_grid()
print "New Grid"
skip = raw_input("Press enter to continue...or enter another key to skip")

printed_pulses = 0

for i in range(second_iterations):
  if(printMove(neurons,test,grid,printed_pulses)):
    printed_pulses = 0
    test.d = .99  #reward test and start over
    grid = G.Grid(grid_x,grid_y) #create new grid
    grid.print_grid()
    print "New Grid"
    skip = raw_input("Press enter to continue...or enter another key to skip")
  else:
    printed_pulses +=1 









