import Connection_List as CL
import Hebbian_List as HL

import numpy
#the neuron used
#learns from reinforcement of current dopamine levels
#looks for difference in d rather than presence
class Neuron:
    
    #initialize the neuron
    #will usually not be called with connections
    def __init__(self, name, layer,height, d_init, threshold, connections = None, exciting = True, output = None,hebbianIncrease=None, p_init = 0):
      self.name = name #for printing
      self.layer = layer #input = 0, output = width, hidden
      self.height = height #instance of neuron in a layer
      self.d_last = d_init #the last level of d is the starting level
      self.p = p_init #starting potential in neurons
      self.connection_list = CL.Connection_List( connections) #will add the connections if they exist, other wise it will be a place holder
      self.reward = False
      self.threshold = threshold
      self.exciting = exciting #false means it will inhibit
      self.hebbian_list = HL.Hebbian_List() #list for tracking what neurons helped cause this one to fire 
      self.last_fired_time = 0
      self.firing_period = 1 #the time between firing on average
      self.firing_period_weight = 10 #the number of previous fires to weigh in average
      self.reward_list = False
      self.hebbian_limit = 5 #the time between firing to trigger hebbian enforcment: currently system for time is badly formed,  where bigger networks dont behave like you would expect of time
      self.output = output
      self.hebbianIncrease = hebbianIncrease
      #self.inhibit = 
    
    #helper function to add connections to given neuron  
    def addConnections(self,neurons, weight = None,time = 0):
      #for each neuron in the array of neurons given
      for neuron in neurons:
        #add the neuron to conncetion list
        #should put in an option to set weight
        self.connection_list.addNode(neuron,weight,time)
        
    def printConnections(self):
      #start with the first connection
      connection = self.connection_list.getHead()
      #print off all the connections
      while connection != None:
        if(self.exciting):
          print self.layer,self.name, " --> ",connection.getNeuron().layer,connection.getNeuron().name, "  w=",connection.getWeight()
        else:
          print self.layer,self.name, " --> ",connection.getNeuron().layer,connection.getNeuron().name, "  w=-", connection.getWeight()
        

        connection = connection.getNext()

        
    def addReward(self):
      self.reward = 1

    def addOutput(self,output):
      self.output = output
        
    #set the internal potential of this neuron
    def setPotential(self,potential):
      self.p = potential
    
    #add the given potential to given neurons potential  
    def addPotential(self,potential):
      self.p += potential
      if self.p < -1:
        self.p = -1
      
    def getPotential(self):
      return self.p
      
    def getDLast(self):
      return self.d_last
      
    def setDLast(self,d):
      self.d_last = d
      
    def getLastFiredTime(self):
      return self.last_fired_time

    def drainPotential(self,time):

      

      #the new potential is the current minus the average rate in
      #the second part makes the subtraction go to zero to prevent the neuron from never firing
      #the.9 makes it decrease always
      if(time-self.last_fired_time != 0):
        new_potential = self.getPotential()*.9-((time-self.last_fired_time)/self.firing_period)*pow((self.firing_period/(time-self.last_fired_time)),2)
      
      else:
        return

      if(new_potential <0):
        new_potential = 0



      self.setPotential(new_potential)


    #ATTENTION
    def addHebbian(self,neuron,connection):
      self.hebbian_list.addNode(neuron,connection)

    def hebbian_enforce(self):

      current_node = self.hebbian_list.getHead()

      while current_node != None:
        
        current_neuron = current_node.connection.getNeuron()

        if (self.last_fired_time - current_neuron.getLastFiredTime()) <= self.hebbian_limit:
          
          if(current_node.origin.exciting):
            #enforce connection
            #print "increase"
            current_node.hebbianIncrease()

          else:
            #discourage negative neuron connection
            #print "decrease"
            current_node.hebbianDecrease()
        current_node = current_node.getNext()


    
    #fires a neuron, passing potential to connected neurons  
    def fire(self,d,new_list,time):
      #print(d)
      
      #set potential to zero since it is firing
      #which means it could loop forever if you let it
      self.setPotential(0)

      #the period is set on the average time between fires
      self.firing_period = ((self.firing_period *self.firing_period_weight)+(time-self.last_fired_time))/(self.firing_period_weight+1)

      #make sure to do before hebbian
      self.last_fired_time = time

      #modify connections for hebian
      #if(d != 0): #without this, low degradation 0 state is nullified
      self.hebbian_enforce()

      self.hebbian_list.empty()
      

      #get the first neuron in connection
      current_connection = self.connection_list.getHead()
      last_connection = None
      #print current_connection

      #will loop over all connections
      #print current_connection
      while current_connection != None:
      
        #current_connection.getNeuron().drainPotential(time)

        #excite or inhibit
        if(self.exciting):
          #add the weight to the potential of connected neuron
          current_connection.getNeuron().addPotential(
            current_connection.getWeight())
        else:
          current_connection.getNeuron().addPotential(
            -current_connection.getWeight()
          )
     
        #Add this neuron to the list of neurons that fired recently for the sake of hebian enforcement
        current_connection.getNeuron().addHebbian(self,current_connection)

        #print(current_connection.getNeuron().getPotential())
        
        #add the neuron to the new firing list if it would at this point
        if current_connection.getNeuron().getPotential() >= self.threshold:
          new_list.addNode(current_connection.getNeuron())

        #removed to have learning be negative as well!!!!  
        #update the weight and the d of the neuron connected to
        #the old method where weight was updated as it fired.
        #if (d <= self.d_last):
        #  if(current_connection.updateWeight(self,d,time)):
        #    if(last_connection == None):
        #      self.connection_list.setHead(current_connection.getNext())
        #      
        #    else:
        #      last_connection.setNext(current_connection.getNext())
        #  else:
        #    last_connection = current_connection

        #move to the next connection
        current_connection = current_connection.getNext()

      
      #update D
      self.setDLast(d)

      #print self.d_last

      ##NOW determined in run by the output  
      #add dopamine to the system
      #if(self.reward != None):
        #d = numpy.tanh(numpy.arctanh(d) + (d + self.reward))

      return self.output