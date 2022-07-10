#load maze.jpg and use thresholding to find the path
import cv2
import numpy as np
import pygame
import heapq

img=cv2.imread('Box.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)

# kernel=np.ones((3,3),np.uint8)
# erosion=cv2.erode(thresh,kernel,iterations=25)
# cv2.imwrite('thresh_erosion.jpg',erosion)
# thresh=erosion
# save thresh image
cv2.imwrite('thresh.jpg',thresh)

pygame.init()
img=pygame.image.load('thresh.jpg')
screen=pygame.display.set_mode((img.get_width(),img.get_height()))
screen.blit(img,(0,0))
running=True
endpoints=[]
while running and len(endpoints)<2:
    if pygame.event.get(pygame.QUIT):
        running=False
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        while True:
            if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                pos=pygame.mouse.get_pos()
                break
        endpoints.append(pos)
        pygame.draw.circle(screen,(0,0,0),pos,5)
  #  pygame.draw.circle(screen,(0,0,0),pos,5)
    pygame.display.flip()
start,end=endpoints
#pygame.quit()
#start,end=(273, 76),(894, 394)
def is_obstacle_2(start,end):
    dx=end[0]-start[0]
    dy=end[1]-start[1]
    if thresh[start[1],start[0]]==0:
        return True
    if thresh[end[1],end[0]]==0:
        return True
    # if the line segment is vertical
    if start[1]<end[1]:
            kk=1
    else:
        kk=-1
    if dx==0:
        for y in range(start[1],end[1],kk):
            if thresh[y,start[0]]==0:
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
            if thresh[y,x]==0:
                return True
        return False
    else:
        if start[1]<end[1]:
            kk=1
        else:
            kk=-1
        for y in range(start[1],end[1],kk):
            x=int((y-start[1])/m+start[0])
            if thresh[y,x]==0:
                return True
        return False    


# find path from start to end using A* algorithm
def manhattan_distance(start,end):
    return pow(abs(start[0]-end[0])**2+abs(start[1]-end[1])**2,0.5)
  #  return abs(start[0]-end[0])+abs(start[1]-end[1])
    #return max(abs(start[0]-end[0]),abs(start[1]-end[1]))

import time
start_time=time.time()
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
heapq.heappush(heap,(manhattan_distance(start,end),0,start,[start]))
visited=set()
found=-1
while heap:
    cost,path_cost,pos,path=heapq.heappop(heap)
    if pos==end:
        found=path_cost
        break
    if pos in visited:
        continue
    visited.add(pos)
    for dx,dy in dx4:
        new_pos=(pos[0]+dx,pos[1]+dy)
        if new_pos[0]<0 or new_pos[0]>=img.get_width() or new_pos[1]<0 or new_pos[1]>=img.get_height() or is_obstacle_2(pos,new_pos):
            continue
        if thresh[new_pos[1],new_pos[0]]==0:
            continue
        if new_pos in visited:
            continue
        new_cost=path_cost+manhattan_distance(pos,new_pos)
        heapq.heappush(heap,(new_cost+manhattan_distance(new_pos,end),new_cost,new_pos,path+[new_pos]))


# img=pygame.image.load('thresh.jpg')
# screen=pygame.display.set_mode((img.get_width(),img.get_height()))
# screen.blit(img,(0,0))

if found==-1:
    print("No Path Found")
else:
    for pos in range(len(path)-1):
        # draw line from pos to pos+1
        pygame.draw.line(screen,(255,0,0),path[pos],path[pos+1],1)
        # draw circle at pos
        # pygame.draw.circle(screen,(0,0,0),pos,5)
    pygame.display.flip()
print("Path Length: ",path_cost)
print("--- %s seconds ---" % (time.time() - start_time))
x=input()


# Somehow, as the size of box increases, the path length decreases.
# But there is a huge tradeoff as when the box size is increased, the time taken to find the path increases exponentially.
