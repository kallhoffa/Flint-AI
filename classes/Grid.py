import random
import sys

class Grid():

  def __init__(self,width = 2, height = 2):

    self.width = width
    self.height = height
    self.grid = [['X' for y in range(height)] for x in range(width)]

    #i = random.randint(0,width-1)
    #j = random.randint(0,height-1)
    i = 0 #testing if it can do well with same conditions
    j = random.randint(0,0)

    self.grid[i][j] = 'G'
    self.goal_x = i
    self.goal_y = j

    a = random.randint(0,width-1)
    b = random.randint(0,height-1)
    while(a == i):
      a = random.randint(0,width-1)
    while(b == j):
      b = random.randint(0,height-1)
    
    #testing if it can do well with same conditions
    a = 2
    b = 2

    self.grid[a][b] = 'F'

    self.F_x = a
    self.F_y = b

    #self.print_grid()

  #output is if you want to print the graph after
  def move(self,movements,output,pulses):

    moved = True #goes false if no movement was allowed
    goal = False

    up = False
    down = False
    right = False
    left = False

    for move in movements:
      if move == 0:
        up = True
      elif move == 1:
        down = True
      elif move == 2:
        right = True
      elif move == 3:
        left = True

    #is there even a move attempted    
    if(up - down != 0 or right - left != 0):
      new_x = self.F_x + right - left
      new_y = self.F_y + up - down
      #if both moves, or just one are allowed
      if (new_x >= 0 and new_x < self.width) and (new_y >=0 and new_y < self.height): 
        self.grid[self.F_x][self.F_y] = 'X'
        self.grid[self.F_x + right - left][self.F_y + up - down] = 'F'

        self.F_x = self.F_x + right - left
        self.F_y = self.F_y + up - down
      
      elif ((left or right) and not (left and right)and new_x >= 0 and new_x < self.width):
          self.grid[self.F_x][self.F_y] = 'X'
          self.grid[self.F_x + right - left][self.F_y] = 'F'

          self.F_x = self.F_x + right - left

      elif ((up or down) and not (up and down) and new_y >=0 and new_y < self.height):
          self.grid[self.F_x][self.F_y] = 'X'
          self.grid[self.F_x][self.F_y + up - down] = 'F'

          self.F_y = self.F_y + up - down

      #no allowable move
      else:
        moved = False
    #no move attempted    
    else:
      moved = False

    #if were at the goal, return true
    if self.F_x == self.goal_x and self.F_y == self.goal_y:
        self.grid[self.F_x][self.F_y] = 'W'
        goal = True

    #if we want an output and we moved, print the grid
    if(output and moved):
      
      self.print_grid()
      print "Pulse #" + str(pulses)
      skip = raw_input("Press enter to continue...or enter another key to skip")
      

  #should return true if at goal, false if not
    return goal

  def print_grid(self):
    sys.stdout.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    for x in range(self.width):
      for y in range(self.height):
        sys.stdout.write(self.grid[x][y])
      sys.stdout.write('\n')



    



