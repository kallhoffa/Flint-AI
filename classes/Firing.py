#doubly linked shouldnt be needed anymore since the threshold check is done before firing now
class Firing():
  
  #creates a node for the firing list
  #INPUTS:
  #  neuron - the neuron queued to fire
  #OUTPUTS:
  #  creates a Firing obj
  def __init__(self,neuron):
    self.neuron = neuron #the neuron to fire
    self.next_firing = None #what would be the next neuron
    self.last_firing = None #what would be the previous neuron
    
  def setNext(self,neuron):
    self.next_firing = neuron
    
  def getNext(self):
    return self.next_firing
    
  def setLast(self, neuron):
    self.last_firing = neuron
  
  def getLast(self):
    return self.last_firing
    
  def getNeuron(self):
    return self.neuron
  