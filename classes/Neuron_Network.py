import random
import numpy
import Firing_List as FL
import Neuron as N
import re

class Neuron_Network:
  
  d_init = 0.5 #initial dopamine levels in neurons
  threshold = 0.5  #the threshold for firing
  d = d_init  #the current level of d, starts at intial
  absorb = .1  #absorption rate of d, percentage of current d
  REWARD = 0.8 #dont think this matters for grid, since reward is given elsewhere
  NORMAL_GROWTH_CHANCE = 0.0005
  DESPERATE_GROWTH_CHANCE = 0.005
  INITIAL_P_GROWTH = 0.35
  HEBBIAN_INCREASE = 0.1
  sensitiviy = 1 #effectiveness of dopamine drop
  D_MIN = .0001
  D_MAX = .9999  
  INHIBITING_CHANCE = .1

  #try making this dependent on number of layers
  LEARNING_TIME = 4
  #best stats for 2 starting posistions
  #re .6
  # normal growth 0.000001
  # desperate 0.005
  # hebian .05

  #WHY IS ABSOPTION WAY HIGHER THAN REWARD?
  #Favors ditching connections when result is 50 50 or lower
  
  
  PRINT_SPACING = 10000
  PERCENT_SPACING = 5000
  
  
  success_percent = 0
  time = 0
  last_print_time = time
  PRINT_GAP = 0
  PERCENT_GAP = 0
  successes = 0
  last_successes = 0
  count = 0
  last_count = 0
  rewarding = 0;

  
  
  
  #starting the network
  def __init__(self):
      self.firing_list = FL.Firing_List() #only thing not started elsehwere
      #self.neuron_list = FL.Firing_List() #complete list of neurons for printing
      self.neuron_layers = [] #complete list of neurons in more graphical form

      self.recently_fired = FL.Firing_List() #the list of neurons that have fired recenlty. for reward tracking

  def getHI(self):
    return self.HEBBIAN_INCREASE
  
  #setup that looks to see if the network can learn to turn on lights when given an on signal
  def simple_light_setup(self):


    N.Neuron("n_1",self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE)
    self.neuron_list.addNode(n_1)

    n_2 = N.Neuron("n_2",self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE)
    self.neuron_list.addNode(n_2)

    n_3 = N.Neuron("n_3",self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE)
    self.neuron_list.addNode(n_3)

    #n_4 = N.Neuron("n_4",self.d,self.threshold,exciting=False)
    #self.neuron_list.addNode(n_4)
    
    #connections just form a line
    n_1.addConnections([n_2,n_4])
    n_2.addConnections([n_3])
    n_4.addConnections([n_3])

    #add rewarding neurons
    n_3.addReward()

    return self.neuron_list

  def save(self,output_file, neurons):
    print "saved", output_file

    f = open(output_file,'w')

    f.write("inputs: " + str(self.inputs) + "\n")
    f.write("hidden_layers: " + str(self.hidden_layers) + "\n")
    f.write("hidden_width: " + str(self.hidden_width) + "\n")
    f.write("outputs: " + str(self.outputs) + "\n")

    for x in range (self.hidden_layers+2):
      for y in range(len(neurons[x])):
        f.write(str(x)+"x"+str(y)+"y"+str(neurons[x][y].p)+"p"+str(neurons[x][y].exciting)+"e: ")
        negative = 1
        if not neurons[x][y].exciting:
          negative = -1
        current_connection = neurons[x][y].connection_list.getHead()
        while current_connection != None:
          weight ='%.10f' %( current_connection.getWeight() * negative)
          f.write(str(weight)+"w"+str(current_connection.getNeuron().layer)+"x"+str(current_connection.getNeuron().height)+"y ")
          current_connection = current_connection.getNext()
        f.write("\n")

    f.close()

  def load(self, input_file):

    dimensions = False
    connections = []

    f = open(input_file,'r')

    i = 0
    for line in f:
      if i == 0:
        self.inputs = int(re.search("inputs: (.+)",line).group(1))
      elif i == 1:
        self.hidden_layers = int(re.search("hidden_layers: (.+)",line).group(1))
      elif i == 2:
        self.hidden_width = int(re.search("hidden_width: (.+)",line).group(1))
      elif i == 3:
        self.outputs = int(re.search("outputs: (.+)",line).group(1))
      else:
        if not dimensions:
          input_neurons = []
          
          hidden_neurons = [[0 for y in range(0,self.hidden_width)] for x in range(0,self.hidden_layers)]
          output_neurons = []
          connections.append([])
          for y in range(self.inputs):
            connections[0].append(0)
          for x in range(self.hidden_layers):
            connections.append([])
            for y in range(self.hidden_width):
              connections[x+1].append(0)
          connections.append([])
          for y in range(self.outputs):
            connections[self.hidden_layers+1].append(0)
          dimensions = True

        both = re.search("(.+)x(.+)y(.+)p(.+)e:",line)
        x = int(both.group(1))
        y = int(both.group(2))
        p = float(both.group(3))
        e = str(both.group(4))

        if(x == 0):
          input_neurons.append(N.Neuron("input "+ str(y),x,y,self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE, p_init = p))
        elif(x == self.hidden_layers+1):
          output_neurons.append(N.Neuron("output "+ str(y),x,y,self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE, p_init = p))
        else:
          
          if e == 'True':
            excite = True
          else :
            excite = False
            #current setup wouldn't work with more complex layouts
          hidden_neurons[x-1][y]=N.Neuron("hidden "+ str(y),x,y,self.d,self.threshold,exciting = excite, hebbianIncrease = self.HEBBIAN_INCREASE, p_init = p)

        connections[x][y] = re.findall("([\w.]+)w(\d+)x(\d+)y",line)
      i += 1
    f.close()

    self.neuron_layers.append(input_neurons)

    for i in range(0,self.hidden_layers):
      self.neuron_layers.append(hidden_neurons[i])

    self.neuron_layers.append(output_neurons)

    #add rewarding neurons
    for i in range(0,self.outputs):
      output_neurons[i].addOutput(i)

    for x in range(len(connections)):
      for y in range(len(connections[x])):
        for i in range(len(connections[x][y])):
          target_neuron = self.neuron_layers[int(connections[x][y][i][1])][int(connections[x][y][i][2])]
          self.neuron_layers[x][y].addConnections([target_neuron],float(connections[x][y][i][0]))

  
    return (self.neuron_layers)





#----------------------------------------------------------------------------------
# COMPLEX lights
#----------------------------------------------------------------------------------
  #reward if matching output
  def complex_light_setup(self,inputs,outputs,hidden_layers, hidden_width):

    self.inputs = inputs
    self.outputs = outputs
    self.hidden_layers = hidden_layers
    self.hidden_width = hidden_width

    input_neurons = []
    hidden_neurons = [[0 for y in range(0,self.hidden_width)] for x in range(0,self.hidden_layers)]
    output_neurons = []
    
    
    
    for i in range(0,self.inputs):
      input_neurons.append(N.Neuron("input "+ str(i),0,i,self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE))
      #self.neuron_list.addNode(input_neurons[i])

    for j in range(0,self.outputs):
      output_neurons.append(N.Neuron("output "+ str(j),self.hidden_layers+1,j,self.d,self.threshold,hebbianIncrease =self.HEBBIAN_INCREASE))
      #self.neuron_list.addNode(output_neurons[j])

    

    for x in range(0,self.hidden_layers):
      for y in range(0,self.hidden_width):
        i = random.uniform(0,1)

        excite = True
        if i <= self.INHIBITING_CHANCE:
          excite = False

        hidden_neurons[x][y]=N.Neuron("hidden "+ str(y),x+1,y,self.d,self.threshold,exciting = excite, hebbianIncrease = self.HEBBIAN_INCREASE)
        #self.neuron_list.addNode(hidden_neurons[x][y])
        #for m in range(0,self.outputs):
          #hidden_neurons[x][y].addConnections([output_neurons[m]])
        #for n in range(0,self.inputs):
          #input_neurons[n].addConnections([hidden_neurons[x][y]])

    #hidden_neurons.append(N.Neuron("hidden "+ str(3), self.d, self.threshold))
    #hidden_neurons[0].addConnections([output_neurons[0]])
    #input_neurons[0].addConnections([hidden_neurons[0]])

    
    self.neuron_layers.append(input_neurons)

    for i in range(0,self.hidden_layers):
      self.neuron_layers.append(hidden_neurons[i])

    self.neuron_layers.append(output_neurons)

    #add rewarding neurons
    for i in range(0,self.outputs):
      output_neurons[i].addOutput(i)

    #self.printNetwork()

    return self.neuron_layers
#------------------------------------------------------------------------------------------------
  def reverse_setup(self):

    n_1 = N.Neuron("n_1",self.d,self.threshold)
    self.neuron_list.addNode(n_1)

    n_2 = N.Neuron("n_2",self.d,self.threshold)
    self.neuron_list.addNode(n_2)

    n_3 = N.Neuron("n_3",self.d,self.threshold)
    self.neuron_list.addNode(n_3)

    n_4 = N.Neuron("n_4", self.d.self.threshold)
    self.neuron_list.addNode(n_4)
    
    #connections just form a line
    n_1.addConnections([n_2])
    n_2.addConnections([n_3])
    n_1.addConnections([n_4])
    n_4.addConnections([n_3])
    
    #add rewarding neurons
    n_3.addReward()

    return self.neuron_list


    
  #causes speficic neurons to fill with potential and fire  
  def pulse(self, neurons, potentials,rewards):
    

    #for each neuron and corresponding potential, fill it
    for neuron, potential in zip(neurons, potentials):
      #fill the neurons
      neuron.setPotential(potential)
      #if that potential would make them fire, add them to the list to start it
      if neuron.getPotential() >= self.threshold:
        self.firing_list.addNode(neuron)
    
    #let the network run until firing stops
    outputs = self.run(rewards)

    return outputs

  #has a chance of 
  def growConnection(self,neuron):

    #more adventurous if at 0 d
    if (self.d == 0): 
      grow = self.DESPERATE_GROWTH_CHANCE
    else:
      grow = self.NORMAL_GROWTH_CHANCE
    

    i = random.uniform(0,1)

    if i <= grow:
      #print "growth"
      
      next_layer = neuron.layer+1
      #range doesn't include the number, random does
      random_neuron = random.randint(0,len(self.neuron_layers[next_layer])-1)
      #new random makes connections first near itself rather than unformily random.triangular(low, high, mode)
      #random_neuron = random.triangular(0,len(self.neuron_layers[next_layer])-1,)
      neuron.addConnections([self.neuron_layers[next_layer][random_neuron]],self.INITIAL_P_GROWTH,self.time) #addConnections prevents duplicates
      #for j in range(0,self.hidden_width):
        #if it is a neuron from the first layer, connect to the second
        #if neuron == self.neuron_layers[0][j]:
        #  neuron.addConnections([self.neuron_layers[1][random.randint(0,self.hidden_width-1)]],self.INITIAL_P_GROWTH,self.time)
          #if it is a neuron from the second layer, connect to the third
      #for j in range(0,self.outputs):
        #if neuron == self.neuron_layers[1][j]:
        #  neuron.addConnections([self.neuron_layers[2][random.randint(0,self.outputs-1)]],self.INITIAL_P_GROWTH,self.time)
      #neuron.addConnections([self.neuron_layers[2][random.randint(0,2)]])
  
  #runs until network stops firing 
  #will update d level, firing from firing list, and print
  def run(self,rewards):
    
    outputs = []
    
    multiple = False
    goal = False
    
    #-------------
    #STRENGTHEN
    #-------------
    #if the d level is peaked, reward the neurons 
    #if (self.recently_fired.getHead() != None and self.recently_fired.getHead().getNeuron().d_last < self.d):
    #  self.recently_fired.strengthen(self.d, self.time,self.LEARNING_TIME)
    
    #--------
    #update
    #---------
    #try updating all the time, might not work...
    

    #print self.rewarding

    #create the list that will populate as neurons fill past threshold
    new_firing_list = FL.Firing_List()

    
    #print "number of pulses", self.time  

    #will end immediately if the firing list is empty,
    #will run if no more neurons will fire
    #this is the whole pulse
    while self.firing_list.isEmpty() is not True:
      self.time += 1
      self.recently_fired.strengthen(self.d, self.time,self.LEARNING_TIME)
      #while the current list is not empty
      #this is each tic
      #so fire all, then this will go again to fire all, until it all escapes out outputs
      while self.firing_list.isEmpty() is not True:
        

        #if it should still fire, fire
        if(self.firing_list.getHead().getNeuron().getPotential() >= self.threshold):

          #make new connection  
          #NOTE UNNESSARY FUNCTION CALLS HAPPENING
          if self.firing_list.getHead().getNeuron().output == None:
            self.growConnection(self.firing_list.getHead().getNeuron())

          #currently adds nodes twice
          if(not self.firing_list.getHead().getNeuron().reward_list):
            self.recently_fired.addNode(self.firing_list.getHead().getNeuron()) #add this recently fired node to those recently fired
            self.firing_list.getHead().getNeuron().reward_list = True
          
          output = self.firing_list.fire_top(self.d,new_firing_list, self.time)
          
          #now done below
          #if(new_d != None):
            #self.d = new_d

          if (output != None):
            outputs.append(output)

        #if it shouldn't fire, just remove it
        else:
          self.firing_list.pop()

      if rewards != None:    
        #test all the outputs for this pulse to see if they match the rewards
        for criteria in rewards:
          for output in outputs:
            #if(output != criteria and goal == True):
              #print "multiple"
              #multiple = True
            if(output == criteria and multiple == False):
              goal = True
              #print "goal"
            elif (output != criteria):
              multiple = True
              #print "goal"
      output = None

      #increment the time for hebian learning metho
      #print self.time
            #change the current firing list to be those     
      self.firing_list = new_firing_list
      
      #self.recently_fired.expiration(self.time,self.LEARNING_TIME)
      #print self.rewarding


    #d decreases by the absoption rate
    #this should happen every pulse
    #self.d = self.d - self.absorb*self.d
    
    #----------------
    #Antiquated - Dont use this reward with grid
    #----------------

    #reward only if it gives one reward. 
    #only really useful for this scenario
    if(goal == True and multiple == False):
      #print(self.d)
      #print goal, multiple
      #for output in outputs:
      #print output
      #self.neuron_layers[1][2].printConnections()
      #rint "\n"
      
      #self.printNetwork()
      #print "\n"
      if (self.d < self.D_MIN):
        self.d = self.D_MIN
      if(self.d > self.D_MAX):
        self.d = self.D_MAX
      self.d = numpy.tanh(numpy.arctanh(self.d) + (self.d + self.REWARD*self.sensitiviy))
      #print "okay?"
      #if (self.d < self.D_MIN):
      #  self.d = self.D_MIN
      
      #if(self.d == numpy.tanh(numpy.arctanh(self.d) + self.REWARD*self.sensitiviy)):
      #  print self.d
      self.successes += 1

    #------------
    #Draining - goes down always when doing the grid
    #--------------
    else:
      #d decreases by the absoption rate
      #this should happen only if goal not met

     
      self.d = self.d - self.absorb*self.d/(2*(1-self.d))
      #adds a minimum so zero level behavior happens faster
      if(self.d < self.D_MIN):
        self.d = 0

      
    #f(self.time >= (self.last_print_time + self.PERCENT_GAP)):
      

    if(self.time >= (self.last_print_time + self.PRINT_SPACING)):
      self.calculatePercent()
      #self.printNetwork()

          
    return outputs

  def calculatePercent(self):
    if(self.count-self.last_count != 0):
      self.success_percent = float(self.successes - self.last_successes) / (self.count - self.last_count)
    self.last_count = self.count
    self.last_successes = self.successes


  def printNetwork(self):
    #put in printing   
    self.last_print_time = self.time
    print "time is ", self.time
    print "successes = ", self.successes
    print "success percent =", str(self.success_percent)
    for x in range(len(self.neuron_layers)):
      for y in range(len(self.neuron_layers[x])):
        self.neuron_layers[x][y].printConnections() 

    #print "absorb = ", self.absorb
    #print "REWARD = ", self.REWARD
    #print "growth chance = ", self.NORMAL_GROWTH_CHANCE
    #print "hebbian increase = ", self.HEBBIAN_INCREASE
    #print "sensitiviy = ", self.sensitiviy  
    print "\n"

  def evolving(self):

    rewards = []
    rewards.append(0)

    last_percent = 0

    while self.success_percent <= .95:

      if(last_percent > self.success_percent):

        if i == 0:
          self.absorb = self.absorb + j*self.absorb*(.01)
        elif i ==1:
          self.REWARD = self.REWARD + j*self.REWARD*(.01)
        elif i ==2:
          self.GROWTH_CHANCE = self.GROWTH_CHANCE + j*self.GROWTH_CHANCE*(.01)
        elif i ==3:
          self.HEBBIAN_INCREASE = self.HEBBIAN_INCREASE + j*self.HEBBIAN_INCREASE*(.01)
        elif i ==4:
          self.sensitiviy = self.sensitiviy + j*self.sensitiviy*(.01)

      elif (self.success_percent < last_percent or self.success_percent == 0):
        
        i = random.randint(0,5)
        j = random.choice([-1,1])

        if i == 0:
          self.absorb = self.absorb + j*self.absorb*(.001)
        elif i ==1:
          self.REWARD = self.REWARD + j*self.REWARD*(.001)
        elif i ==2:
          self.GROWTH_CHANCE = self.GROWTH_CHANCE + j*self.GROWTH_CHANCE*(.001)
        elif i ==3:
          self.HEBBIAN_INCREASE = self.HEBBIAN_INCREASE + j*self.HEBBIAN_INCREASE*(.001)
        elif i ==4:
          self.sensitiviy = self.sensitiviy + j*self.sensitiviy*(.001)

      last_percent = self.success_percent
      self.pulse([self.neuron_layers[0][0]],[1],rewards)
      self.count += 1

    print "absorb = ", self.absorb
    print "REWARD = ", self.REWARD
    print "growth chance = ", self.GROWTH_CHANCE
    print "hebbian increase = ", self.HEBBIAN_INCREASE
    print "sensitiviy = ", self.sensitiviy