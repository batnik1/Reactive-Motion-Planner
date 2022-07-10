#load maze.jpg and use thresholding to find the path
from collections import defaultdict
import cv2
from cv2 import exp
from matplotlib.patches import Polygon
import numpy as np
import pygame
import heapq
import math
import random
from test import *
# import priority queue
import heapq
import time
from test2 import *



img=cv2.imread('White.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)


# save thresh image
cv2.imwrite('thresh.jpg',thresh)

corners=[]
for i in range(thresh.shape[0]):
    for j in range(thresh.shape[1]):
        if thresh[i,j]==0:
            # check all 8 neighbors
            dir=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
            if thresh[i,j]==255:
                continue
            count=0
            for k in range(8):
                x,y=j+dir[k][0],i+dir[k][1]
                if x<0 or y<0 or x>=thresh.shape[1] or y>=thresh.shape[0]:
                    continue
                if thresh[y,x]==255:
                    count+=1
            if count==5 or count==1:
                corners.append((j,i))



pygame.init()
img=pygame.image.load('thresh.jpg')
#screen=pygame.display.set_mode((img.get_width(),img.get_height()))
#screen.blit(img,(0,0))

# for i in corners:
#     #pyga.draw.circle(screen,(0,0,255),(i[0],i[1]),3)
# #pyga.display.flip()

# size of image
width=img.get_width()
height=img.get_height()
#print(width,height)


def is_not_obstacle(start,end):
    # check if any point between has a white pixel or not
    if thresh[start[1],start[0]]==255 or thresh[end[1],end[0]]==255:
        return False
    qu=[(start,end)]
    while len(qu)>0:
        start,end=heapq.heappop(qu) 
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            continue
        mid=(start[0]+end[0])//2,(start[1]+end[1])//2
        if thresh[mid[1],mid[0]]==255:
            return False
        heapq.heappush(qu,(start,mid))
        heapq.heappush(qu,(mid,end))
    return True

edges_full=[]
edge_dic=defaultdict(list)

for i in corners:
    x1,y1=i
    # find edges 
    for j in corners:
        if i==j:
            continue
        x2,y2=j
        # call is not_obstacle function
        if is_not_obstacle((x1,y1),(x2,y2)):
            edges_full.append(((x1,y1),(x2,y2)))

coroners=[]
# all corners in list
for i in corners:
    x,y=i
    coroners.append((x,y))

new_edges=[]
waste_edges=[]
edge_dic=defaultdict(set)
for edge in edges_full:
    x1,y1=edge[0]
    x2,y2=edge[1]
    # see if the edge is horizontal or vertical
    way=""
    if x1==x2:
        way="vertical"
    elif y1==y2:
        way="horizontal"
    else:
        way="diagnol"
    # travel from one end to other and see if the value is same or not
    flag=False
    count=0
    faulty=0
    # see value of thresh at edge points
    #print(x1,y1,x2,y2,thresh[y1,x1],thresh[y2,x2])
    for i in range(min(x1,x2)+2,max(x1,x2)-2):
        # check both directions
        if (i,y1) in coroners:
            #print(x1,y1,x2,y2)
            count+=1
            # check up and down
            #print(thresh[(y1-1,x1)])
            ##pyga.draw.circle(screen,(255,255,0),(i,y1),1)
            # flag=True
            # break
        temp=0
        #print(thresh.shape,thresh[y1,x1])
        if y1-1<0 or y1-1>=thresh.shape[0]:
            temp+=1
        else:
            if thresh[(y1-1),i]==255:
                temp+=1
        if y1+1<0 or y1+1>=thresh.shape[0]:
            temp+=1
        else:
            if thresh[(y1+1),i]==255:
                temp+=1
      #  print(temp,"temp")
        if temp!=1:
            faulty+=1
    for i in range(min(y1,y2)+2,max(y1,y2)-2):
        if (x1,i) in coroners:
            count+=1
            #pygame.draw.circle(screen,(255,255,0),(x1,i),1)
            # flag=True
            # break
        temp=0
        if x1-1<0 or x1-1>=thresh.shape[1]:
            temp+=1
        else:
            if thresh[i,x1-1]==255:
                temp+=1
        if x1+1<0 or x1+1>=thresh.shape[1]:
            temp+=1
        else:
            if thresh[i,x1+1]==255:
                temp+=1
        if temp!=1:
            px=temp
            faulty+=1

   # print(count)
    if count<1 and way!="diagnol" and faulty<1:
        new_edges.append(edge)

for edge in new_edges:
    x1,y1=edge[0]
    x2,y2=edge[1]
    # draw a line there
    #pygame.draw.line(screen,(0,255,0),(x1,y1),(x2,y2),2)
    #pygame.display.flip()

edges=set()
for edge in new_edges:
    x1,y1=edge[0]
    x2,y2=edge[1]
    # choose min and max
    ex=[(x1,y1),(x2,y2)]
    ex.sort()
    x1,y1=ex[0]
    x2,y2=ex[1]
    edges.add(((x1,y1),(x2,y2)))
    edge_dic[(x1,y1)].add(((x1,y1),(x2,y2)))
    edge_dic[(x2,y2)].add(((x1,y1),(x2,y2)))
new_edges=list(edges)
#print(new_edges)
# see polygons from these edges
# start from a corner and go to one of its edge, it it returns to the corner, it is a polygon
visited={}
visi_edge={}
for i in corners:
    x,y=i
    visited[(x,y)]=False

Polygons=[]
for vertice in corners:
    if visited[vertice]==True:
        continue
    heap=[]
    heapq.heappush(heap,vertice)
    polygon=[vertice]
    while len(heap)>0:
        vertice_move=heapq.heappop(heap)
       # print(edge)
        x1,y1=vertice_move
        visited[(x1,y1)]=True
        explore_edges=list(edge_dic[(x1,y1)])
        explore_edges_1=explore_edges[0]
        explore_move_1=explore_edges_1[0] if explore_edges_1[0]!=(x1,y1) else explore_edges_1[1]
        explore_edges_2=explore_edges[1]
        explore_move_2=explore_edges_2[0] if explore_edges_2[0]!=(x1,y1) else explore_edges_2[1]
        #print(vertice_move)
        if visited[explore_move_1]==True and visited[explore_move_2]==True:
           # polygon.append(vertice_move)
            Polygons.append(polygon)
            break
        vertice_move=explore_move_1 if visited[explore_move_1]==False else explore_move_2
        polygon.append(vertice_move)
        heapq.heappush(heap,vertice_move)


        # wait for 1 sec sing #pygame
       # #pygame.time.wait(1000)
print(Polygons,"polygon")

# save the #pygame image
#pygame.image.save(screen,"edges.png")



# # input()
def f(point1,point2,safety_distance,constant):
    dist=math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    if point1[0]==point2[0] and point1[1]==point2[1]:
        return math.inf
    else:
        f_x=constant*(1/safety_distance-1/dist)*(1/pow(dist,3))*(point1[0]-point2[0])
        f_y=constant*(1/safety_distance-1/dist)*(1/pow(dist,3))*(point1[1]-point2[1])
    return [f_x,f_y]
def attractive_force(point1,point2,constant):
    # constant*(q-q')
    f_x=constant*(point1[0]-point2[0])#+constant
    f_y=constant*(point1[1]-point2[1])#+constant
    return [-f_x,-f_y]
def force(endpoint,points_f,box):
    forces=[]
    safety_distance=1000
    constant=0.1
    for point in points_f:
        f_x,f_y=f(endpoint,point,safety_distance,constant)
        forces.append((f_x,f_y))
    for point in box:
        f_x,f_y=f(endpoint,point,safety_distance,1)
        forces.append((f_x,f_y))
    # sum all forces
    f_x=0
    f_y=0
    for force in forces:
        f_x+=force[0]
        f_y+=force[1]
    return [-1*f_x,-1*f_y]
"""
# draw a point 
points_f=[]
endpoints=[]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            endpoints.append((x,y))
            pygame.draw.circle(screen,(0,0,255),(x,y),5)
            pygame.display.flip()
            if len(endpoints)==2:
                running=False
                break

prev=endpoints[0]
goal=endpoints[1]
while True:
    prev_x,prev_y=prev
    pygame.draw.circle(screen,(255,255,255),(x,y),5)
    pygame.display.flip()
    x,y=endpoints[0]
    pygame.draw.circle(screen,(0,0,255),(x,y),5)
    pygame.display.flip()
    # see min dist with each edge in polygon from every polygon
    for polygon in Polygons:
        minpoint=(0,0)
        min_dist=math.inf
        exes=[]
        for i in range(len(polygon)):
            exes.append((polygon[i],polygon[(i+1)%len(polygon)]))
        # print(exes)
        for edge in exes:
            dist,neare=pnt2line(endpoints[0],edge[0],edge[1])
           # print(edge,endpoints)
            if dist<min_dist:
                minpoint=neare
                min_dist=dist
        #    input()
        print(min_dist)
        pygame.draw.circle(screen,(255,0,0),minpoint,5)
        pygame.display.flip()
        points_f.append(minpoint)
    forc=force(endpoints[0],points_f)
    mag=math.sqrt(forc[0]**2+forc[1]**2)
    print("MAG",mag)
    # draw a arrow in the direction of force
    angle=math.atan2(forc[1],forc[0])
    # draw a arrow of size 10 in the direction of force
    pygame.draw.line(screen,(255,0,0),endpoints[0],(endpoints[0][0]+10*math.cos(angle),endpoints[0][1]+10*math.sin(angle)),2)
    pygame.display.flip()
    # attract to goal
    forced=attractive_force(endpoints[0],endpoints[1],0.0000001)
    maga=math.sqrt(forced[0]**2+forced[1]**2)
    print("MAG_ATT",maga)
    # draw a arrow in the direction of force
    angle=math.atan2(forced[1],forced[0])
    # draw a arrow of size 10 in the direction of force
    pygame.draw.line(screen,(0,255,0),endpoints[0],(endpoints[0][0]+10*math.cos(angle),endpoints[0][1]+10*math.sin(angle)),2)
    pygame.display.flip()
    # forc[0]=-forced[0]+forc[0]
    # forc[1]=-forced[1]+forc[1]
    # move endpoint by force
    forc=[forced[0]+forc[0],forced[1]+forc[1]]
    magx=math.sqrt(forc[0]**2+forc[1]**2)
    print("MAGX",magx)
    
    endpoints[0]=(endpoints[0][0]+forc[0]/magx*10,endpoints[0][1]+forc[1]/magx*10)
    # wait for 1 sec sing pygame
    pygame.time.wait(100)
"""
