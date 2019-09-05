import Firing as F

#list of neurons that need to be fired. 
#should check if the neuron needs to fire before firing
class Firing_List():
  
  #doubly linked list since it will need to remove from middle
  def __init__(self,nodes=None):
    if(nodes == None):
      self.head = None
      self.tail = None
    else:
      self.head = nodes[0]
      self.tail = nodes[len(nodes)-1]
    self.tick = 0

  
  #add firing node to the end of the list
  def addNode(self,neuron):
    new_node = F.Firing(neuron)

    if(self.isEmpty()):
      self.head = new_node
    if(self.tail != None):
      self.tail.setNext(new_node)
    new_node.setLast(self.tail)
    self.tail = new_node
    
  #remove top element
  def pop(self):
    self.head = self.head.getNext()
    
  #remove selected node
  def remove(self,node): #BAAAADDDD
    if(node.getLast() == None):
      self.pop()
    else:
      node.getLast().setNext(node.getNext())
    #node.getNext().setLast(node.getLast())
    #
  
  #checks if there is a list
  def isEmpty(self):
    if self.head == None:
      return True
    else:
      return False
      
  def getHead(self):
    return self.head
      
  #tells the top node to fire with new d level and list to put it in after
  def fire_top(self,d,new_list,time):
    
    #fire the top node, which sends weights to next neuron, adds that to the firing list if it should be, and updates the weights and d level
    output = self.getHead().getNeuron().fire(d,new_list,time)
    #new_list.addNode(self.head)
    
    #pop the top for the firing list
    self.pop()

    return output

  #def expiration(self, time, learning_time):
  #  while ((self.getHead() != None) and (self.getHead().getNeuron().last_fired_time #<= (time - learning_time))):
  #    self.getHead().getNeuron().reward_list = False
  #    self.pop()


  #strengthens the weight of connections of neurons that fired before a reward happened
  #can also degrade
  def strengthen(self, d, time,learning_time):
    
    current_node = self.getHead()
    #print "strengthen"
    #i = 0
    #j = 0
    #while current_node!= None:
    #  i+=1
    #  if not current_node.getNeuron().reward_list:
    #    j+= 1
    #  current_node = current_node.getNext()
    #print current_node
    
    ##print "reward list that shouldnt be", j
    #print "number in reward list", i
    #current_node = self.getHead()

    while current_node != None:
      
      #the neuron fired longer ago than the learning time allows
      if (time - current_node.getNeuron().last_fired_time) > learning_time:
        #print "remove"
        current_node.getNeuron().reward_list = False #it is no longer flagged as on the list
        #previous_node = current_node #the current node is recorded as previous
        #current_node = current_node.getNext() #the node we are looking for is now the next one
        #self.remove(previous_node) #remove the node that expired from this list

        ##BAAADDD COOOD
        self.pop()  #should be fine since its first in first out
        current_node = self.getHead()
        
      #elif(time- current_node.getNeuron().last_fired_time == 1):
        #print "just made"
        #print current_node.getNeuron().connection_list.getHead()
      else:
        current_connection = current_node.getNeuron().connection_list.getHead()
        previous_connection = None
        #if current_connection == None:
          #print "no connections
        #if current_node.getNeuron().connection_list.connection_count>0:
          #print current_node.getNeuron().connection_list.connection_count
        while current_connection != None:
          #true means theconnection should be dropped
          #print "update weight"
          if(current_connection.updateWeight(current_node.getNeuron(),d,time)):
            if(previous_connection == None):
              current_node.getNeuron().connection_list.head=current_connection.getNext()
              current_node.getNeuron().connection_list.connection_count -= 1
            else:
              previous_connection.setNext(current_connection.getNext())
              current_node.getNeuron().connection_list.connection_count -= 1
          #the previous only changes if the current doesn't drop
          else:
            previous_connection = current_connection
          
          current_connection = current_connection.getNext()
        #print current_node.getNeuron().connection_list.connection_count  
        current_node = current_node.getNext()
      
    return 
  
  def print_list(self):
    current_node = self.getHead()
    while(current_node != None):
      print(current_node.getNeuron().name)
      current_node = current_node.getNext()
