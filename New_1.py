from distutils.command.config import config
import cv2
import numpy as np
import pygame
import heapq
from Agent import *
img=cv2.imread('Box.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)
pygame.init()
img=pygame.image.load('thresh.jpg')
screen=pygame.display.set_mode((img.get_width(),img.get_height()))
screen.blit(img,(0,0))

configuration_map=cv2.imread('configuration_map.jpg')
gray=cv2.cvtColor(configuration_map,cv2.COLOR_BGR2GRAY)
ret,configuration_map=cv2.threshold(gray,127,255,0)
# make configuration map for radius r as a image
# check collision of a circle of r radius with black pixels
def robot_config(pos,radius):
    # return all the points occupied by the robot
    points=set()
    flag=1
    for i in range(pos[0]-radius,pos[0]+radius):
        for j in range(pos[1]-radius,pos[1]+radius):
            if (i-pos[0])**2+(j-pos[1])**2<radius**2:
                if i>=0 and i<img.get_width() and j>=0 and j<img.get_height():
                    if thresh[j,i]==0:
                        flag=0
                        break
                    else:
                        points.add((i,j))
        if flag==0:
            break
    if flag==0:
        return False
    return points
def manhattan_distance(start,end):
    return pow(abs(start[0]-end[0])**2+abs(start[1]-end[1])**2,0.5)
def is_obstacle_2(start,end):
    dx=end[0]-start[0]
    dy=end[1]-start[1]
    if configuration_map[start[1],start[0]]==0:
        return True
    if configuration_map[end[1],end[0]]==0:
        return True
    # if the line segment is vertical
    if start[1]<end[1]:
            kk=1
    else:
        kk=-1
    if dx==0:
        for y in range(start[1],end[1],kk):
            if configuration_map[y,start[0]]==0:
                return True
        return False
    m=dy/dx
    if abs(m)<1:
        if start[0]<end[0]:
            kk=1
        else:
            kk=-1
        for x in range(start[0],end[0],kk):
            y=int(m*(x-start[0])+start[1])
            if configuration_map[y,x]==0:
                return True
        return False
    else:
        if start[1]<end[1]:
            kk=1
        else:
            kk=-1
        for y in range(start[1],end[1],kk):
            x=int((y-start[1])/m+start[0])
            if configuration_map[y,x]==0:
                return True
        return False
# configuration_map=np.zeros((img.get_height(),img.get_width()),dtype=np.int)
# for i in range(img.get_width()):
#     for j in range(img.get_height()):
#         points=robot_config((i,j),5)
#         if points==False:
#             configuration_map[j,i]=0
#         else:
#             configuration_map[j,i]=255
#     cv2.imwrite('configuration_map.jpg',configuration_map)

n=20
# make n random bots
bots=[]
for i in range(n):
    while True:
        x=np.random.randint(0,img.get_width())
        y=np.random.randint(0,img.get_height())
        # check (x,y) in configuration_map
        if configuration_map[y,x]==255:
            agent=Agent((x,y))
            bots.append(agent)
            break
 # choose goals for bots
for i in range(n):
    while True:
        x=np.random.randint(0,img.get_width())
        y=np.random.randint(0,img.get_height())
        # check (x,y) in configuration_map  
        if configuration_map[y,x]==255:
            bots[i].goal=(x,y)
            break



# show them on map
screen.blit(img,(0,0))
# for agent in bots:
#     pygame.draw.circle(screen,(0,0,0),agent.pos,5)
#     pygame.draw.circle(screen,(255,255,0),agent.goal,5)
pygame.display.flip()
# run the simulation
remove=[]
remove_line=[]

while True:
   # screen.blit(img,(0,0))
    for bot in bots:
        if bot.path==[]:
            while True:
                # new goal
                x=np.random.randint(0,img.get_width())
                y=np.random.randint(0,img.get_height())
                # check (x,y) in configuration_map
                if configuration_map[y,x]==255:
                    bot.goal=(x,y)
                    break
            #pygame.draw.circle(screen,(255,255,0),agent.goal,5)
            # A* from bot.pos to bot.goal
            stack=[]
            heapq.heappush(stack,(0,bot.pos))
            visited=set()
            visited.add(bot.pos)
            box=3
            # store all the possible directions in dx4
            dx4=[]
            for i in range(box):
                for j in range(box):
                    if i-box//2==0 and j-box//2==0:
                        continue
                    dx4.append((i-box//2,j-box//2))
                    #print(dx4)
                    #dx4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
                    heap=[]
                    heapq.heappush(heap,(manhattan_distance(bot.pos,bot.goal),0,bot.pos,[bot.pos]))
                    visited=set()
                    found=-1
            while heap:
                cost,path_cost,pos,path=heapq.heappop(heap)
                if pos==bot.goal:
                    found=path_cost
                    break
                if pos in visited:
                    continue
                visited.add(pos)
                for dx,dy in dx4:
                    new_pos=(pos[0]+dx,pos[1]+dy)
                    if new_pos[0]<0 or new_pos[0]>=img.get_width() or new_pos[1]<0 or new_pos[1]>=img.get_height() or is_obstacle_2(pos,new_pos):
                        continue
                    if configuration_map[new_pos[1],new_pos[0]]==0:
                        continue
                    if new_pos in visited:
                        continue
                    new_cost=path_cost+manhattan_distance(pos,new_pos)
                    heapq.heappush(heap,(manhattan_distance(new_pos,bot.goal),new_cost,new_pos,path+[new_pos]))
            if found==-1:
                print('no path')
                bot.path=[]
            bot.path=path[::-1]
            bot.I=len(path)-1
            # draw path
            # for i in range(len(path)-1):
            #     pygame.draw.line(screen,(0,0,255),path[i],path[i+1],1)
            pygame.display.flip()
            
            
        else:
            # move bot
          #  print("A")
            if bot.goal!=bot.path[0]:
                print("F")
            pygame.draw.circle(screen,(255,255,0),bot.goal,5)
            for i in range(0,bot.I,4):
                pygame.draw.line(screen,(255,0,0),bot.path[i],bot.path[i+1],1)
            bot.pos=bot.path[bot.I-1]
            bot.I-=1
            if bot.I==0:
                bot.path=[]
                bot.I=0
            # clear earlier bot from screen
            pygame.draw.circle(screen,(255,255,255),bot.early,5)
            pygame.draw.circle(screen,(0,0,0),bot.pos,5)
            pygame.display.flip()
            bot.early=bot.pos
            
    
    

input()