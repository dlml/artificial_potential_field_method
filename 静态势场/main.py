"""
Main script

Contains
-------
Functions
    draw and __main__

Author
-------
Faizan Ali(nccvector)

"""

import numpy as np 
import cv2
import math
import random

from positional import *
from objects import *

# Main
if __name__ == '__main__':
    # Defining world dimensions
    #world_size = (640, 480)
    world_size = (800,800)
    # Initializing blank canvas with white color
    image = np.ones((world_size[1],world_size[0],3),dtype=np.uint8) * 255
    #background color
    image[:,:] = [245,245,245]

    #line color
    x_line = list(range(0,800,20))
    y_line = list(range(0,800,20))

    image[x_line,:] = [128,128,128]
    image[:,y_line] = [128,128,128]

    # Defining agent and goal
    agent = Agent(Position(40, 40), scan_radius=20, possible_moves=4)
    goal = Goal(Position(640, 640), sigma=math.sqrt(world_size[0]**2 + world_size[1]**2))

    # Defining obstacles in a list
    sigma_obstacles = 5
    obstacles = [Obstacle(Position(240, 180), sigma=sigma_obstacles),
                Obstacle(Position(240, 280), sigma=sigma_obstacles),
                Obstacle(Position(240, 380), sigma=sigma_obstacles),
                Obstacle(Position(340, 180), sigma=sigma_obstacles),
                Obstacle(Position(340, 280), sigma=sigma_obstacles),
                Obstacle(Position(340, 380), sigma=sigma_obstacles),
                Obstacle(Position(580, 580), sigma=sigma_obstacles),]
    #draw_radius=4*sigma_obstacles), 


    # Drawing objects
    agent.draw(image)
    goal.draw(image)
    for obstacle in obstacles:
        obstacle.draw(image)

    # Displaying initial frame and wait for intial key press
    cv2.imshow('Output', image)
    cv2.waitKey(1000)

    cost_weight  = 20

    cost = 0
    visited_list = []
    count = 0

    while Position.calculate_distance(agent.position, goal.position) > 10:

        possible_moves = agent.get_possible_moves()
        min_value = math.inf
        best_move = possible_moves[0] # initializing best move with first move
        # Finding move with the least value
        for move in possible_moves:
            move_value = goal.get_attraction_force(move)
            for obstacle in obstacles:
                move_value += obstacle.get_repulsion_force(move)
            
            if PtoXY(move) in visited_list:
                move_value += 1
                print("test")

            if move_value < min_value:
                min_value = move_value
                best_move = move

                visited_list.append(PtoXY(move))
                #move.visit += 1

            print("value_",move_value)
        print("best_move",best_move.x,best_move.y)
        print("new move")
        
        # p = random.randint(-2,2)
        # if count%5 == 0:
        #     newPosition = Position(obstacles[6].position.x + p*40,obstacles[6].position.y+ p*20)
        #     obstacles[6].move(image,newPosition)
        #     obstacles[6].position = newPosition
        # count += 1
        
        # Setting best move as agent's next position
        agent.position = best_move

        #last_positon  = 

        '''
        As we are not clearing up the initial frame at every iteration
        so we do not need to draw static objects again and again

        '''
        agent.draw(image)

        # Displaying updated frame
        cv2.imshow('Output', image)
        k = cv2.waitKey(20)
        if k == 27:
            break
    
    # Hold on last frame
    cv2.waitKey(0)
        
        