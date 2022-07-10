#load maze.jpg and use thresholding to find the path
import cv2
import numpy as np
import pygame
import heapq
from scipy.signal import savgol_filter

img=cv2.imread('Box.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)

# save thresh image
cv2.imwrite('thresh.jpg',thresh)
# print dimensions of the thresh
print(thresh.shape)
# use erosion on the thresh image and save it as thresh_dilation.jpg
kernel=np.ones((3,3),np.uint8)
erosion=cv2.erode(thresh,kernel,iterations=25)
cv2.imwrite('thresh_erosion.jpg',erosion)
thresh=erosion



pygame.init()
img=pygame.image.load('thresh_erosion.jpg')
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
#start,end=(92, 38),(585, 321)
def is_obstacle_2(start,end):
    qu=[(start,end)]
    while len(qu)>0:
        start,end=heapq.heappop(qu)
        if thresh[start[1],start[0]]==0:
            return True
        if thresh[end[1],end[0]]==0:
            return True
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            continue
        mid=(start[0]+end[0])//2,(start[1]+end[1])//2
        if thresh[mid[1],mid[0]]==0:
            return True
        heapq.heappush(qu,(start,mid))
        heapq.heappush(qu,(mid,end))
    return False

# find path from start to end using A* algorithm
def manhattan_distance(start,end):
    return pow(abs(start[0]-end[0])**2+abs(start[1]-end[1])**2,0.5)
  #  return abs(start[0]-end[0])+abs(start[1]-end[1])
    #return max(abs(start[0]-end[0]),abs(start[1]-end[1]))


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
        if new_pos[0]<0 or new_pos[0]>=img.get_width() or new_pos[1]<0 or new_pos[1]>=img.get_height():
            continue
        if thresh[new_pos[1],new_pos[0]]==0:
            continue
        if new_pos in visited:
            continue
        new_cost=path_cost+manhattan_distance(pos,new_pos)
        heapq.heappush(heap,(new_cost+manhattan_distance(new_pos,end),new_cost,new_pos,path+[new_pos]))



if found==-1:
    print("No Path Found")
    exit()

def points_path(start,end):
    dx=end[0]-start[0]
    dy=end[1]-start[1]
    points=[]
    # return the points on the path from start to end
    # if the line segment is vertical
    if dx==0:
        if start[1]<end[1]:
            kk=1
        else:
            kk=-1
        for y in range(start[1],end[1],kk):
            points.append((start[0],y))
        return points
    m=dy/dx
    if abs(m)<1:
        if start[0]<end[0]:
            kk=1
        else:
            kk=-1
        for x in range(start[0],end[0],kk):
            y=int(m*(x-start[0])+start[1])
            points.append((x,y))
    else:
        if start[1]<end[1]:
            kk=1
        else:
            kk=-1
        for y in range(start[1],end[1],kk):
            x=int((y-start[1])/m+start[0])
            points.append((x,y))
    return points


points=[]
for pos in range(len(path)-1):
    # Append all the points of line segment from path[pos] to path[pos+1]
    points+=points_path(path[pos],path[pos+1])
    # draw circle at pos
    # pygame.draw.circle(screen,(0,0,0),pos,5)
    pygame.display.flip()


img=pygame.image.load('thresh.jpg')
screen=pygame.display.set_mode((img.get_width(),img.get_height()))
screen.blit(img,(0,0))

points=sorted(list(set(points)))
# Sample points from points list
points=points[::20]
pointx=[]
pointy=[]
for pos in points:
    pointx.append(pos[0])
    pointy.append(pos[1])
    # pygame.draw.circle(screen,(255,0,0),pos,1)
    # pygame.display.flip()

kk=len(pointx)
t=kk//2
if t%2==0:
    t+=1
y_filtered = savgol_filter(pointy, t, 2)
print(y_filtered)

for pos in range(len(points)-1):
    xx=(points[pos][0],y_filtered[pos])
    yy=(points[pos+1][0],y_filtered[pos+1])
    pygame.draw.line(screen,(0,0,0),xx,yy,3)
    # draw circle at pos
    pygame.draw.circle(screen,(255,0,0),xx,5)
    pygame.draw.line(screen,(255,0,0),points[pos],points[pos+1],3)
    pygame.display.flip()

x=input()
pygame.quit()
