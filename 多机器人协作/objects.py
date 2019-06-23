"""
Objects script

Contains
-------
Classes
    Agent, Obstacle and Goal

Author
-------
Faizan Ali(nccvector)

"""

import math
import cv2
from positional import Position
import random

# Agent class for Agent attributes
class Agent:
    """
    Creates an Agent object
    
    Parameters
    ----------
    position : Position
        Position of agent in world
    scan_radius : int, optional
        Step size of agent, by default 1
    possible_moves : int, optional
        Number of point generated around agent, by default 6
    draw_radius : int, optional
        Radius for visualization, by default 5
    draw_color : tuple, optional
        Color for visulization, by default (255,0,0)

    """

    def __init__(self, position, scan_radius=1, possible_moves=20, draw_radius=20, draw_color=(46,139,87),sigma = 1):
        
        # Property attributes
        self.position = position
        self._scan_radius = scan_radius
        self._possible_moves = possible_moves
        self._sigma = sigma

        # Visual attributes
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        #cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        cv2.rectangle(image,(x1,y1),(x1+self._draw_radius,y1+self._draw_radius),self._draw_color,-1)
   
    def get_possible_moves(self):
        """
        Makes a list of points around agent
        
        Returns
        -------
        list
            List of points around agent

        """

        angle_increment = (2*math.pi)/self._possible_moves # 2pi/n
        angle = -angle_increment # Going one step negative to start from zero
        possible_moves_list = []
        for _ in range(self._possible_moves):
            # Starting from angle 0
            angle += angle_increment
            possible_moves_list.append(Position(self._scan_radius * math.cos(angle) + self.position.x,self._scan_radius * math.sin(angle) + self.position.y))
            #possible_moves_list.append(Position(self.position.x))
        return possible_moves_list

    def get_force(self, position):
        
        
        dist_value = -1.1*(1/(self._sigma*math.sqrt(2*math.pi))) * math.exp(-(Position.calculate_distance_squared(position,self.position)/(2*self._sigma*self._sigma)))
        '''
        if self.position.calculate_distance(position) > 300:
            dist_value = 1.02*dist_value

        elif self.position.calculate_distance(position) >= 200:
            dist_value = 1.009*dist_value
        elif self.position.calculate_distance(position) < 20:
            #dist_value = 0.7*dist_value
            dist_value = -1*dist_value

        else :
            dist_value = 1.08*dist_value
        '''
        if self.position.calculate_distance(position) < 80:
            dist_value = -1*dist_value

        print(self.position.calculate_distance(position))
        #print(dist_value)


        return dist_value


# Obstacle class for repulsion based objects


class ByAgent:
    """
    Creates an ByAgent object
    
    Parameters
    ----------
    position : Position
        Position of agent in world
    scan_radius : int, optional
        Step size of agent, by default 1
    possible_moves : int, optional
        Number of point generated around agent, by default 6
    draw_radius : int, optional
        Radius for visualization, by default 5
    draw_color : tuple, optional
        Color for visulization, by default (255,0,0)

    """

    def __init__(self, position, scan_radius=1, possible_moves=20, draw_radius=20, draw_color=(255,215,0)):
        
        # Property attributes
        self.position = position
        self._scan_radius = scan_radius
        self._possible_moves = possible_moves

        # Visual attributes
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        #cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        cv2.rectangle(image,(x1,y1),(x1+self._draw_radius,y1+self._draw_radius),self._draw_color,-1)
   
    def get_possible_moves(self):
        """
        Makes a list of points around agent
        
        Returns
        -------
        list
            List of points around agent

        """

        angle_increment = (2*math.pi)/self._possible_moves # 2pi/n
        angle = -angle_increment # Going one step negative to start from zero
        possible_moves_list = []
        for _ in range(self._possible_moves):
            # Starting from angle 0
            angle += angle_increment
            possible_moves_list.append(Position(self._scan_radius * math.cos(angle) + self.position.x,self._scan_radius * math.sin(angle) + self.position.y))
            #possible_moves_list.append(Position(self.position.x))
        return possible_moves_list

# Obstacle class for repulsion based objects
class Obstacle:
    """
    Creates an Obstacle object
    
    Parameters
    ----------
    position : Position
        Position of Obstacle in the world
    mu : int, optional
        Peak of distribution, by default 1
    sigma : int, optional
        Spread of distribution, by default 1
    draw_radius : int, optional
        Radius for visualization, by default 5
    draw_color : tuple, optional
        Color for visualization, by default (0,0,255)
        
    """

    def __init__(self, position, mu=1, sigma=1, draw_radius=40, draw_color=(255,99,71)):

        # Property attributes
        self.position = position
        self.originPosition = position
        self.lastposition = position
        self._mu = mu
        self._sigma = sigma
        
        # Visual attributes
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        #cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)
        y1 = int(self.position.y)

        cv2.rectangle(image,(x1,y1),(x1+self._draw_radius,y1+self._draw_radius),self._draw_color,-1)
        #line_type,shift)

    # Attribute type function
    def get_repulsion_force(self, position):
        """
        Repulsion force calculation function
        
        Parameters
        ----------
        position : Position
            Position of cell to check force at
        
        Returns
        -------
        double
            The value of repulsion at cell

        """

        # Implementing repulsion equation
        #dist_value = 0
        '''
        position_list_cal = [self.position,Position(self.position.x+20,self.position.y),Position(self.position.x,self.position.y+20),Position(self.position.x+20,self.position.y+20)]
        dist_value = 0
        for Ever_position in position_list_cal:
            dist_value += (1/(self._sigma*math.sqrt(2*math.pi))) * math.exp(-(Position.calculate_distance_squared(Ever_position,position)/(2*self._sigma*self._sigma)))
        '''
        #center  = Position(self.position.x+20,self.position.y+20)
        dist_value = (1/(self._sigma*math.sqrt(2*math.pi))) * math.exp(-(Position.calculate_distance_squared(self.position,position)/(2*self._sigma*self._sigma)))
        
        return dist_value
    def move(self,image,toPosition):
        x1 = int(toPosition.x)
        y1 = int(toPosition.y)

        cv2.rectangle(image,(x1,y1),(x1+self._draw_radius,y1+self._draw_radius),self._draw_color,-1)
        cv2.rectangle(image,(self.position.x,self.position.y),
                            (self.position.x+self._draw_radius,self.position.y+self._draw_radius),
                            (255,255,255),-1)
        x_line = list(range(0,800,20))
        y_line = list(range(0,800,20))

        image[x_line,:] = [128,128,128]
        image[:,y_line] = [128,128,128]

        self.lastposition = self.position

        self.position = toPosition


    def randMove(self,image):
        p = random.randint(0,3)
        angle_increment = (2*math.pi)/4 # 2pi/n
        angle = -angle_increment # Going one step negative to start from zero
        possible_moves_list = []
        for _ in range(4):
            # Starting from angle 0
            angle += angle_increment
            possible_moves_list.append(Position(40 * math.cos(angle) + self.position.x,40* math.sin(angle) + self.position.y))
            #possible_moves_list.append(Position(self.position.x))

        toPosition = possible_moves_list[p]
        while abs(toPosition.x- self.originPosition.x) > 80 or  abs(toPosition.y- self.originPosition.y) > 80:
            p = random.randint(0,3)
            toPosition = possible_moves_list[p]
        print(toPosition.x,toPosition.y)
        self.move(image,toPosition)
        #self.position = toPosition

    def move_speed(self,image,direction,speed):
        angle_increment = (2*math.pi)/4 # 2pi/n
        angle = -angle_increment # Going one step negative to start from zero
        angle = angle + direction*angle_increment
        print(angle)
        
        toPosition = Position(40 *speed* math.cos(angle) + self.position.x,40*speed* math.sin(angle) + self.position.y)

        
        self.move(image,toPosition)




# Goal class for Goal object
class Goal:
    """
    Creates a Goal object
    
    Parameters
    ----------
    position : Position
        Position of Goal in the world
    mu : int, optional
        Peak of distribution, by default 1
    sigma : int, optional
        Spread of distribution, by default 1
    draw_radius : int, optional
        Radius for visualization, by default 5
    draw_color : tuple, optionalVisit https://qiao.github.io/PathFinding.js/visual/
        Color for visualization, by default (0,255,0)
        
    """

    def __init__(self, position, mu=1, sigma=1, draw_radius=20, draw_color=(128,0,0)):

        # Property attributes
        self.position = position
        self._mu = mu
        self._sigma = sigma

        # Visual attributes
        self._draw_radius = draw_radius
        self._draw_color = draw_color

    def draw(self, image):
        #cv2.circle(image, (int(self.position.x), int(self.position.y)), self._draw_radius, self._draw_color, -1)  # Fill
        x1 = int(self.position.x)
        y1 = int(self.position.y)

        cv2.rectangle(image,(x1,y1),(x1+self._draw_radius,y1+self._draw_radius),self._draw_color,-1)

    # Attribute type function
    def get_attraction_force(self, position):
        """
        Attraction force calculation function
        
        Parameters
        ----------
        position : Position
            Position of cell to check force at
        
        Returns
        -------
        double
            The value of attraction at cell

        """

        # Implementing attraction equation
        dist_value = -(1/(self._sigma*math.sqrt(2*math.pi))) * math.exp(-(Position.calculate_distance_squared(self.position,position)/(2*self._sigma*self._sigma)))
        return dist_value
