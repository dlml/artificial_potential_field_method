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

def testCrash(position1,position2):
    return 0

def get_chang(Obstacles,goal,image):
    
    x_line = list(range(0,800,20))
    y_line = list(range(0,800,20))
    value_mat = np.zeros([len(x_line),len(y_line)])
    #print(value_mat.shape)
    for x in x_line:
        for y in y_line:
            #print(x,y)
            position = Position(x,y)
            value = goal.get_attraction_force(position)
            for obstacle in obstacles:
                value += obstacle.get_repulsion_force(position)
            value_mat[x_line.index(x)][y_line.index(y)] = value
            if(x == 240 and y ==140 or
              x == 180 and y == 380 or 
              x == 340 and y== 440 or
              x ==380 and y==380 or 
              x == 600 and y ==440):
              print(value)
            #print(value)
            #print("yes")
    value_min = value_mat.min()
    value_max = value_mat.max()
    value_mean = np.mean(value_mat)
    print("max",value_max)
    print("min",value_min)
    dif = value_max- value_min
    print(dif)
    x,y =value_mat.shape
    #print(value_min + dif/5*1)


    for i in range(x):
        for j in range(y):
            if value_mat[i,j] <= value_min:
                value_mat[i,j] = 0
                #print("0")
            elif value_mat[i,j] <= value_min + dif/(1.5e4):
                value_mat[i,j] = 1
                #print("1")
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*3.5:
                value_mat[i,j] = 2
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*6:
                value_mat[i,j] = 3
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*8.5:
                value_mat[i,j] = 4
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*11:
                value_mat[i,j] = 5
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*13.5:
                value_mat[i,j] = 6
            elif value_mat[i,j] <= value_min + dif/(1.5e4)*20:
                value_mat[i,j] = 7     
            elif value_mat[i,j] <= 0.00:
                #0.06616
                value_mat[i,j] = 8
            else:
                value_mat[i,j] =9
    print(value_mat)
    print("end")

            
    return value_mat 
        
def draw_chang(image,value_mat):
    x,y =value_mat.shape
    for i in range(x):
        for j in range(y):
            if value_mat[i,j] <= 0:
                #color = (255,245,238)
                color = (0,255,255)
            elif value_mat[i,j] <=1:
                #color = (255,160,122)
                color = (0,69,255)
            elif value_mat[i,j] <=2:
                #color = (255,127,80)
                color = (80,127,255)
            elif value_mat[i,j] <=3:
                #color = (255,69,0)
                color = (0,215,255)
            elif value_mat[i,j] <=4:
                color = (0,255,255)
            elif value_mat[i,j] <=5:
                color = (47,107,85)
            elif value_mat[i,j] <=6:
                color = (87,139,46)
            elif value_mat[i,j] <=7:
                color = (170,178,32)
            elif value_mat[i,j] <=7:
                color = (128,0,128)
            elif value_mat[i,j] <=8:
                color = (79,79,46)
            else :color = (128,0,0)
            cv2.rectangle(image,(i*20,j*20),(i*20+20,j*20+20),color,-1)
            #print("test")
            #print(i,j,color)


    




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
    agent = Agent(Position(80, 80), scan_radius=20, possible_moves=4,sigma=math.sqrt(world_size[0]**2 + world_size[1]**2))
    byagent1 = ByAgent(Position(480, 200), scan_radius=20, possible_moves=4)
    #480 240
    #180 480
    byagent2 = ByAgent(Position(180, 480), scan_radius=20, possible_moves=4)
    byagents = [byagent1,byagent2]
    #540 640
    goal = Goal(Position(640, 740), sigma=math.sqrt(world_size[0]**2 + world_size[1]**2))

    # Defining obstacles in a list
    #
    sigma_obstacles = 6
    '''
    obstacles = [Obstacle(Position(240, 180), sigma=sigma_obstacles),
                Obstacle(Position(240, 380), sigma=sigma_obstacles),
                Obstacle(Position(240, 580), sigma=sigma_obstacles),
                Obstacle(Position(440, 180), sigma=sigma_obstacles),
                Obstacle(Position(440, 380), sigma=sigma_obstacles),
                Obstacle(Position(440, 580), sigma=sigma_obstacles)]
                #Obstacle(Position(580, 580), sigma=sigma_obstacles),]
    #draw_radius=4*sigma_obstacles), 
    '''

    
    obstacles = [Obstacle(Position(240, 140), sigma=sigma_obstacles),
                 Obstacle(Position(180, 380), sigma=sigma_obstacles),
                Obstacle(Position(340, 440), sigma=sigma_obstacles),
                Obstacle(Position(380, 380), sigma=sigma_obstacles),
                Obstacle(Position(600, 440), sigma=sigma_obstacles)

                 ]

    
    


    # Drawing objects
    agent.draw(image)
    byagent1.draw(image)
    byagent2.draw(image)

    goal.draw(image)
    for obstacle in obstacles:
        obstacle.draw(image)

    # Displaying initial frame and wait for intial key press
    cv2.imshow('Output', image)
    cv2.waitKey(1000)
    #1000

    cost_weight  = 20

    cost = 0
    visited_list = []
    count = 0
    direction = 1

    
    while Position.calculate_distance(agent.position, goal.position) > 10:
        
        
        #######agent###########

        possible_moves = agent.get_possible_moves()
        min_value = math.inf
        best_move = possible_moves[0] # initializing best move with first move
        # Finding move with the least value
        for move in possible_moves:
            move_value = goal.get_attraction_force(move)
            for obstacle in obstacles:
                move_value += obstacle.get_repulsion_force(move)
            
            if PtoXY(move) in visited_list:
                move_value + 0.3*abs(move_value)
                #move_value += 1
                print("test")

            if move_value < min_value:
                min_value = move_value
                best_move = move

                visited_list.append(PtoXY(move))
                #move.visit += 1

            print("value_",move_value)
        print("best_move",best_move.x,best_move.y)
        #print("new move")

        # Setting best move as agent's next position
        agent.position = best_move

        #######Byagent###########
        for byagent in byagents:
            possible_moves_by = []

            possible_moves_by = byagent.get_possible_moves()
            min_value_by = math.inf
            best_move_by = possible_moves_by[0] # initializing best move with first move
            # Finding move with the least value
            for move in possible_moves_by:
                move_value = agent.get_force(move)
                for obstacle in obstacles:
                    move_value += obstacle.get_repulsion_force(move)
                
                if PtoXY(move) in visited_list:
                    move_value = move_value + 0.0*abs(move_value)
                    #0.0698
                    print("test")

                if move_value < min_value:
                    min_value = move_value
                    best_move_by = move

                    visited_list.append(PtoXY(move))
                    
            byagent.position = best_move_by

        

    

        #######obstacle###########
        
        
        #random_move
        '''
        if count%5 == 0:
            for everObstacle in obstacles:
                everObstacle.randMove(image)
                #1-right,2-down,3-left,4-up
                #everObstacle.move_speed(image,4,1)
        count += 1
        '''
        
        #move speed
        '''
        
        for everObstacle in obstacles:
            #everObstacle.randMove(image)
            #1-right,2-down,3-left,4-up
            everObstacle.move_speed(image,direction,1)
            if (everObstacle.position.x >= 800 or everObstacle.position.y >= 800 
                or everObstacle.position.x <0 or everObstacle.position.y <0):
                direction = 4-direction
        '''

        '''
        As we are not clearing up the initial frame at every iteration
        so we do not need to draw static objects again and again

        '''

        
        agent.draw(image)
        byagents[0].draw(image)
        byagents[1].draw(image)
        flag_crash = False
        for everObstacle in obstacles:
            #everObstacle.randMove(image)
            if agent.position.calculate_distance(everObstacle.position) < 0:
                flag_crash = True

        if(flag_crash):
            break
        

    #value_mat = get_chang(obstacles,goal,image)
    #draw_chang(image,value_mat)

    # Displaying updated frame
        cv2.imshow('Output', image)
        k = cv2.waitKey(100)
        if k == 27:
            break
        #cv2.destroyAllWindows()

    
    


    
    # Hold on last frame
    cv2.waitKey(0)
        
        