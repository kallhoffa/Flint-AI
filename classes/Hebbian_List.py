
import Hebbian as H

#a singly linked list for all the connections a neuron has
#simulates axon synapeses
class Hebbian_List():
  
  #initialize with head, if connections provided, add the node to the list
  def __init__(self,neuron = None,hebbian=None):
      self.head = None
      if(hebbian != None):
        self.addNode(neuron, hebbian)
  
  #add a connection, in the form of a connection node
  def addNode(self,neuron, connection):
    new_node = H.Hebbian(neuron,connection)
    new_node.setNext(self.head)
    self.head = new_node    
    
  def getHead(self):
    return self.head

  def empty(self):
    self.head = None