import math

#a node for the connection lists, with connected neuron and the weight
class Hebbian():
  
  #creates a new connection, of the neuron receiving signal.
  def __init__(self,neuron, connection):
    self.origin = neuron
    self.hebbian = neuron.hebbianIncrease
    self.connection = connection
    self.next_hebbian = None
    
  def setNext(self,hebbian):
    self.next_hebbian = hebbian
    
  def getNext(self):
    
    return self.next_hebbian

      
  def hebbianIncrease(self):

    import Neuron_Network as NN
    w = self.connection.getWeight()
    
    if w > 0.399:
      return

    if w < 0.0001:
      return

    x = math.log(w/(.4-w))

    d= self.connection.getNeuron().getDLast()
    s = pow(d,2)/pow(1-d,2)
    
    if(.4 / (1 + math.exp(-(x + self.hebbian)))>.4):
       self.connection.setWeight(.399)
    else:
      w =.4 / (1 + math.exp(-(x + self.hebbian*s)))
      #print "heb = ", w, "d^2 = ", pow(self.connection.getNeuron().getDLast(),2)
      self.connection.setWeight( w)
    #print self.connection.neuron.name

    

  def hebbianDecrease(self):

    w = self.connection.getWeight()

    if w > 0.4:
      w = 0.3999

    if w < 0.0001:
      return
      
    x = math.log(w/(1-w))
    hebbian_modifier = .2
    self.connection.setWeight(
      1 / (1 + math.exp(-(x - hebbian_modifier)))
    ) 
