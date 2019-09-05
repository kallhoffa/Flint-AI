import random
import math #for Logs and Exponentionals
import numpy

#a node for the connection lists, with connected neuron and the weight
#FUNCTIONS: 
#init(neuron, w, time)
#setNext(neuron)
#getNext()
#getNeuron()
#getWeight()
#setWeight(w)
#updateWeight(neuron,d,time)

class Connection():

  CONNECTION_MIN = 0.05      #the min weight for a connection before it disconnects
  CONNECTION_MAX = 0.4   #the max weight for a connection. will always reset to this value before progressing
  SENSITIVITY_LENGTH = 100    #the length of time after creation that a connection will be extra sensative to weaken connection
  GROWTH_SENSITIVITY = 50    #the extra sensitiviy to weakening of a newly created connection (was at 5 with only success)
  NORMAL_SENSITIVITY = 1.5            #normal sensitiviy to domanine
  ZERO_SUBTRACTION = 5    #how a connection decays when there is 0 dopamine in the system
  
  #creates a new connection, of the neuron receiving signal.
  #INPUTS:
  #  neuron- a neuron obj, the neuron the connection goes to
  #  w- a float, (0-1),the strength of a connection, positive or negative
  #  time- an int, >0,the time of creation
  #OUTPUTS:
  #  creates a connection with no following connection
  def __init__(self,neuron,w = None,time = 0):
    
    self.neuron = neuron #the neuron connecting to

    #Will make it so initial connnections dont destroy themselves
    if time == 0:
      self.creation_time = -self.SENSITIVITY_LENGTH #should make it so creation_time doesnt conflict in updateWeight
    else:
      self.creation_time = time #time of function is time of creation

    #will assign a random Weight   
    if(w == None):
      self.w = random.uniform(self.CONNECTION_MIN,self.CONNECTION_MAX*.99) #starts with a random weight, weights only greater than 0 with single type neurons
    else:
      self.w = w
    
    self.next_connection = None #there is no next connection in the list
    self.last_connection = None

  #Desc: Sets the next connection in the connection list
  #INPUTS: 
  #   connection- a connection obj, the next connection in the list  
  #OUTPUTS
  #   sets the next connection
  def setNext(self,connection):
    self.next_connection = connection

  def setLast(self, connection):
    self.last_connection = connection
  
  def getLast(self,connection):
    return self.last_connection
  #Desc: Gets the next connection in the connection list
  #INPUTS: 
  #   
  #OUTPUTS
  #   next_connection- a connection obj, the next in the connection list 
  def getNext(self):
    return self.next_connection

  #Desc: Gets the neuron of the connection
  #INPUTS: 
  #     
  #OUTPUTS
  #   neuron-  a neuron obj, the neuron the connection points to    
  def getNeuron(self):
    return self.neuron  

  #Desc: Gets the weight of the connection
  #INPUTS: 
  #    
  #OUTPUTS
  #   w- float, (0-1), the strength of the connection  
  def getWeight(self):
    return self.w

  #Desc: Sets the weight of the connection
  #INPUTS: 
  #   w- float, (0-1),the strength of the connection  
  #OUTPUTS
  #   sets the weight of the conenction
  def setWeight(self, w):
    self.w = w
    
  #Desc: Updates the weight of the connection based on the current time and current dopamine levels.
  #strengthens when dopamine is increasing, weakens otherwise
  #behaves differently at 0 dopamine or with a new connection
  #INPUTS: 
  #   neuron- a neuron obj, the originator of the connection
  #   d- float, ~(0-1), the current level of dopamine in the system
  #   time- int, >0, the current time of the system  
  #OUTPUTS
  #   Boolean- True is the connection needs to be dropped
  #   Updates connection
  def updateWeight(self,neuron,d,time):
    

    #reflection of refract?
    #will exit without updating if the connection is brand new
    if(time - self.creation_time == 0):
      return False
    
    #if the connection is new (created with in window specified), and the dopamine is decreasing
    #CHANGE!!! now anytime the connection is new
    #will set a new sensitivity
    #if(time - self.creation_time < self.SENSITIVITY_LENGTH and d-neuron.getDLast() < 0 ):
    ##if(time - self.creation_time < self.SENSITIVITY_LENGTH ):
      #sensitivity = self.GROWTH_SENSITIVITY
    #else:
      #sensitivity = self.NORMAL_SENSITIVITY

    
    #CONNECTION MAX REPLACING 1 in the formulas

    #instead of black white, make it a scale
    sensitivity = self.NORMAL_SENSITIVITY + self.GROWTH_SENSITIVITY/pow((time - self.creation_time),3)/pow((1-d),2)*pow(d,2) 

    #if(self.w <= 0 or self.w >= self.CONNECTION_MAX):
      #print self.w

    #if sensitivity > 30:
      #print "sensitivity", sensitivity
    
    x = math.log(self.w/(self.CONNECTION_MAX-self.w))

    if (d == 0):
      #print d
      z = self.CONNECTION_MAX / (1 + math.exp(-( x -(self.ZERO_SUBTRACTION))))
      #print z
    else:
      #divide by d to get relative difference (OR NOT! THIS MAKES FOR LIKE - 1000's)
      z = self.CONNECTION_MAX / (1 + math.exp(-( x +((d-neuron.getDLast())*sensitivity))))
    
    if (z > self.w and z > .399999):
      self.w = .399999
    
    else:
      self.w = z
      #print "last D was", neuron.getDLast(), "now D is", d
      #print "heres a new weight", z
  #self.w = numpy.tanh(numpy.arctanh(self.w) + numpy.sign(self.w)*(d-self.neuron.getDLast())*NORMAL_SENSITIVITY)

    
    if(self.w < self.CONNECTION_MIN):
      print "dropped connection"
      return True

    if(self.w  >= self.CONNECTION_MAX):
      self.w = self.CONNECTION_MAX*.999999


    #FURTHER NOTES
    
    #reinforcement algorithim
    #w is enforced if d levels are higher than before
    #w is lessened if d levels are weaker than before
    #w will always be between 0 and 1
    #new rules, 0 to 1, negative is its own neuron type

    #i was using self.getNeuron.getDLast
    #but thats the neuron were going to, not the one updating, so now it passes the correct neuron
