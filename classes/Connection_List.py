import Connection as C

#a singly linked list for all the connections a neuron has
#simulates axon synapeses
class Connection_List():
  
  #creates a new connection list, the head being the first connection
  #INPUTS:
  #  connections - any connection nodes to make up connection list
  #OUTPUTS:
  #  creates a connection list with 0 or more connections
  def __init__(self,connections=None):
      self.head = None #set when a node is added
      if(connections != None): #otherwise it will add None to the list
        for node in connections: #add each connection provided to the list
          self.addNode(node)
      self.connection_count = 0
  
  #using a neuron, creates a new connection node in the connection list, while checking for duplicate connections
  #INPUTS:
  #  neuron- a neuron obj, the neuron the to be connected to
  #  weight- a float, (0-1),the strength of a connection, positive or negative
  #  time- an int, >0,the time of creation
  #OUTPUTS:
  #  appends the new connection to the top of the connection list
  def addNode(self,neuron,weight = None,time=0):
    #check for dupplicate connections
    if self.checkForConnection(neuron):
      new_node = C.Connection(neuron,weight,time) #create a connection obj
      new_node.setNext(self.head) #apppend connection obj to the top of the list
      self.head = new_node #set the new connection as the new head
      self.connection_count += 1

  #using a connection, creates a new connection node in the connection list, while checking for duplicate connections
  #INPUTS:
  #  connection - a connection obj, the one to be added
  #OUTPUTS:
  #  creates a connection with no following connection
 #def addConnection(self,connection):
    #check for dupplicate connections
    #print "add connection"
    #if self.checkForConnection(connection):
      #connection.setNext(self.head) #append connection obj to top of the list
      #self.head = connection #set the new connection as the new head

  #check for duplicate connection in the list
  #INPUTS:
  #  neuron - a neuron obj, the one being searched for
  #OUTPUTS:
  #  T/F: if there is already a connection to the neuron it will return False, otherwise True
  def checkForConnection(self,neuron):
    current_connection = self.head #start at the head
    while current_connection != None: #explore all connections in the list
      if current_connection.getNeuron() == neuron: #if a connection goes to the neuron in question
        return False #return false
      #other wise, go to the next connection
      current_connection = current_connection.getNext()
    return True #if no neuron on the connection list matches given neuron, return True

  def getHead(self):
    return self.head

  def setHead(self, node):
    self.head = node