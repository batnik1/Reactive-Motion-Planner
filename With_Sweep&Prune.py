from collections import defaultdict, deque
from hashlib import new
from operator import ne
import cv2
import numpy as np
import pygame
import heapq
import math
from line_segment import intersect
from line_segment import *

from sklearn import neighbors
from sklearn.metrics import fowlkes_mallows_score

img=cv2.imread('Box.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)



img_thresh=thresh.copy()
# draw 20*20 grid on image and if any pixel in it is black then it is an obstacle
for i in range(0,img.shape[0],10):
    for j in range(0,img.shape[1],10):
        # see if any pixel in it is black
        flag=1
        for k in range(i,i+10):
            if k>=img.shape[0]:
                break
            for l in range(j,j+10):
                if l>=img.shape[1]:
                    break
           #     print(k,l,i,j)
                if thresh[k,l]==0:
                    # draw 20*20 grid on image
                    cv2.rectangle(img_thresh,(j,i),(j+10,i+10),(0,0,0),-1)
                    flag=0
                    break
            if flag==0:
                break
# Make a padding strip of 5 pixel on each side
img_thresh=cv2.copyMakeBorder(img_thresh,5,5,5,5,cv2.BORDER_CONSTANT,value=0)
cv2.imwrite('House2_thresh.png',img_thresh)

# loop around the whole image and check if any pixel is black and any 5 pixel neighborhood is white out of 8.
# if yes then mark as corner
corners=[]
for i in range(img_thresh.shape[0]):
    for j in range(img_thresh.shape[1]):
        if img_thresh[i,j]==0:
            # check all 8 neighbors
            dir=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
            if img_thresh[i,j]==255:
                continue
            count=0
            for k in range(8):
                x,y=j+dir[k][0],i+dir[k][1]
                if x<0 or y<0 or x>=img_thresh.shape[1] or y>=img_thresh.shape[0]:
                    continue
                if img_thresh[y,x]==255:
                    count+=1
            if count==5 or count==1:
                corners.append((j,i))


pygame.init()
screen=pygame.display.set_mode((img_thresh.shape[1],img_thresh.shape[0]))
screen.blit(pygame.image.load('House2_thresh.png'),(0,0))
pygame.display.flip()

#corners=cv2.goodFeaturesToTrack(img_thresh,1000,0.01,10) # image, max number of corners, quality level, min distance between corners
#corners=np.int0(corners)
# draw corners on pygame
for i in corners:
    pygame.draw.circle(screen,(0,0,255),(i[0],i[1]),3)
pygame.display.flip()



def is_not_obstacle(start,end):
    # check if any point between has a white pixel or not
    if img_thresh[start[1],start[0]]==255 or img_thresh[end[1],end[0]]==255:
        return False
    qu=[(start,end)]
    while len(qu)>0:
        start,end=heapq.heappop(qu) 
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            continue
        mid=(start[0]+end[0])//2,(start[1]+end[1])//2
        if img_thresh[mid[1],mid[0]]==255:
            return False
        heapq.heappush(qu,(start,mid))
        heapq.heappush(qu,(mid,end))
    return True

def is_obstacle_2(start,end,f):    # TODO: Use sweep and prune algorithm here
    o_start=start[:]
    o_end=end[:]

    qu=[(start,end)]
    while len(qu)>0:
        start,end=heapq.heappop(qu) 
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            continue
        mid=(start[0]+end[0])//2,(start[1]+end[1])//2
        if img_thresh[mid[1],mid[0]]==0:
            # check if this mid_point is 0 in f(mid_point)
            if f(mid[0])==mid[1]:
                pass
            else:
                # print("HELL no")
                # # draw mid
                # pygame.draw.circle(screen,(0,0,255),(mid[0],mid[1]),4)
                # pygame.display.flip()
                return True
        heapq.heappush(qu,(start,mid))
       # print(qu,mid,end)
        heapq.heappush(qu,(mid,end))
    return False

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

# nearest corners from selection
# running=True
# endpoints=[]
# while running:
#     # selection from mouse 2 points
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             running=False
#         if event.type==pygame.MOUSEBUTTONDOWN:
#             endpoints.append(event.pos)
#             if len(endpoints)==4:
#                 running=False


# # find nearest corners from these and paint them green in pygame
# min_corners=[]
# for i in endpoints:
#     x,y=i
#     min_dist=math.inf
#     min_corner=None
#     for j in coroners:
#         x1,y1=j
#         dist=math.sqrt((x-x1)**2+(y-y1)**2)
#         if dist<min_dist:
#             min_dist=dist
#             min_corner=j
#     pygame.draw.circle(screen,(0,255,0),(min_corner[0],min_corner[1]),10)
#     pygame.display.flip()
#     # print these corners
#     print(min_corner)
#     min_corners.append(min_corner)

# # traverse from min_corners[0] to min_corners[1] given these corners are vertical
# for i in range(min(min_corners[0][1],min_corners[1][1])+1,max(min_corners[0][1],min_corners[1][1])-1):
#     # print side to side neighbors
#     print(i,img_thresh[(i,min_corners[0][0]-1)],img_thresh[(i-1,min_corners[0][0]+1)])    





# input()



# among all these line take only those that have contrasting values on other sides
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
    #print(x1,y1,x2,y2,img_thresh[y1,x1],img_thresh[y2,x2])
    for i in range(min(x1,x2)+2,max(x1,x2)-2):
        # check both directions
        if (i,y1) in coroners:
            #print(x1,y1,x2,y2)
            count+=1
            # check up and down
            #print(thresh[(y1-1,x1)])
            pygame.draw.circle(screen,(255,255,0),(i,y1),1)
            # flag=True
            # break
        temp=0
        #print(img_thresh.shape,img_thresh[y1,x1])
        if y1-1<0 or y1-1>=img_thresh.shape[0]:
            temp+=1
        else:
            if img_thresh[(y1-1),i]==255:
                temp+=1
        if y1+1<0 or y1+1>=img_thresh.shape[0]:
            temp+=1
        else:
            if img_thresh[(y1+1),i]==255:
                temp+=1
      #  print(temp,"temp")
        if temp!=1:
            faulty+=1
    for i in range(min(y1,y2)+2,max(y1,y2)-2):
        if (x1,i) in coroners:
            count+=1
            pygame.draw.circle(screen,(255,255,0),(x1,i),1)
            # flag=True
            # break
        temp=0
        if x1-1<0 or x1-1>=img_thresh.shape[1]:
            temp+=1
        else:
            if img_thresh[i,x1-1]==255:
                temp+=1
        if x1+1<0 or x1+1>=img_thresh.shape[1]:
            temp+=1
        else:
            if img_thresh[i,x1+1]==255:
                temp+=1
        if temp!=1:
            px=temp
            faulty+=1

   # print(count)
    if count<1 and way!="diagnol" and faulty<1:
        new_edges.append(edge)
        edge_dic[(x1,y1)].add(edge)
        edge_dic[(x2,y2)].add(edge)

for edge in new_edges:
    x1,y1=edge[0]
    x2,y2=edge[1]
    # draw a line there
    pygame.draw.line(screen,(0,255,0),(x1,y1),(x2,y2),2)
    pygame.display.flip()



# save the pygame image
pygame.image.save(screen,"edges.png")

# make visibility graph
# remove duplicate entries in edges
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


endpoints_edge=[(25, 15),(25, 565),(785, 565),(785, 15)]

# choose 2 endpoints for start and goal
running=True
endpoints_sg=[]

while running:
    # selection from mouse 2 points
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            endpoints_sg.append(event.pos)
            if len(endpoints_sg)==2:
                running=False


# # Find nearest vertices to each
# for e_e in endpoints_edge:
#     min_dist=math.inf
#     min_vertex=None
#     for vertex in corners:
#         x,y=vertex
#         dist=math.sqrt((e_e[0]-x)**2+(e_e[1]-y)**2)
#         if dist<min_dist:
#             min_dist=dist
#             min_vertex=vertex
#     pygame.draw.circle(screen,(0,255,0),(min_vertex[0],min_vertex[1]),10)
#     pygame.display.flip()
#     print(min_vertex)

# add these endpoints in endpoints_edges
# remove endpoints from corners
corners=list(set(corners)-set(endpoints_edge))
endpoints_edge=endpoints_sg

# print(endpoints_edge)
#endpoints_edge=[(25, 15), (25, 565), (785, 565), (785, 15), (93, 301), (723, 295)]
neighbors=defaultdict(list)
visited=set()
# draw endpoints
for e in endpoints_edge:
    pygame.draw.circle(screen,(0,255,0),e,5)
    pygame.display.flip()

corners+=endpoints_edge
corners=list(set(corners))

new_edges=list(edges)
visibility_graph=defaultdict(list)
for i in corners:
    if i in endpoints_edge:
        continue
    # rotational plane sweep algorithm to find all edges that are visible from this point
    vertices=corners[:]
    # For each vertex vi , calculate αi , the angle from the horizontal axis to the line segment vvi
    vertices_with_angles=[]
    for j in vertices:
        if i==j:
            continue
        x1,y1=i
        x2,y2=j
        alpha=math.atan2(y2-y1,x2-x1)
        if alpha<0:
            alpha+=2*math.pi
        vertices_with_angles.append((j,alpha))
    # sort vertices by angle
    vertices_with_angles.sort(key=lambda x:x[1])
    # Create the active list S, containing the sorted list of edges that intersect the horizontal half-line emanating from v
    # Check which edges are intersecting the horizontal half line from (i) to (infinity,i[1]) 
    checker=((i[0],i[1]),(1000000,i[1]))
    # if the edge is intersecting, add it to the active list
    active_list=[]
    # loop over all edges
    for j in new_edges:
        A,B=checker
        C,D=j
        if intersect(A,B,C,D):
            # also see the distance between i and line CD
            try:
                m=(D[1]-C[1])/(D[0]-C[0])
                c=C[1]-m*C[0]
                r=abs(m*i[0]-i[1]+c)/math.sqrt(m**2+1)
            except:
                r=abs(i[0]-C[0])
            # calculate distance from i to C
            d1=math.sqrt((C[0]-i[0])**2+(C[1]-i[1])**2)
            d2=math.sqrt((D[0]-i[0])**2+(D[1]-i[1])**2)
            # move C towards D a bit
            dx=D[0]-C[0]
            dy=D[1]-C[1]
            C_f=(C[0]+dx/1000,C[1]+dy/1000)
            D_f=(D[0]-dx/1000,D[1]-dy/1000)
            # check dist from i to C_f
            d1_f=math.sqrt((C_f[0]-i[0])**2+(C_f[1]-i[1])**2)
            d2_f=math.sqrt((D_f[0]-i[0])**2+(D_f[1]-i[1])**2)
            if d1_f<d1 and d2_f<d2:
                final=r
            else:
                final=min(d1,d2)
            active_list.append((j,final))
    # sort the active list by distance
    active_list.sort(key=lambda x:x[1])
   # active_list=[active_list[0] for active_list in active_list]
    if len(active_list)==0:
        continue
    # pygame draw the active list
    # for all αi do
    #   if vi is visible to v then
    #       Add the edge (v, vi ) to the visibility graph.
    #if i== (25, 15):
    for j in vertices_with_angles:
        active_list.sort(key=lambda x:x[1])
        #print(active_list)
        x1,y1=i
        x2,y2=j[0]
        alpha=j[1]
        # check if line from i to j intersects wih first edge in active list
        A=i
        B=j[0]
        if len(active_list)==0:
            continue
        C,D=active_list[0][0]
        # draw i and j and line CD
        
        pygame.draw.circle(screen,(255,0,0),(x1,y1),3)
        pygame.draw.circle(screen,(255,255,0),(x2,y2),3)
        pygame.draw.line(screen,(255,0,0),(C[0],C[1]),(D[0],D[1]),2)
        pygame.display.flip()
        #degree
    # print(i,alpha*180/math.pi)
    #     input()
        # move A towardds B a bit
        dx=B[0]-A[0]
        dy=B[1]-A[1]
        A=(A[0]+dx/1000,A[1]+dy/1000)
        B=(B[0]-dx/1000,B[1]-dy/1000)


        if not intersect(A,B,C,D) or (C==B or D==B):
            j_s=j[0]
            niegbors_i=[]
            dir=[(0,1),(1,0),(0,-1),(-1,0)]
            for k in dir:
                x,y=k
                if img_thresh[(i[1]+y),(i[0]+x)]==0:
                    # check its 4 neigbors if any one of them is white then allow
                    count=0
                    new_point=(i[0]+x,i[1]+y)
                    for l in dir:
                        x1_,y1_=l
                        if img_thresh[(new_point[1]+y1_),(new_point[0]+x1_)]==255:
                            count+=1
                    if count==1:
                        niegbors_i.append((i[0]+x,i[1]+y))
            
        #     # same for j
            niegbors_j=[]
            dir=[(0,1),(1,0),(0,-1),(-1,0)]
            for k in dir:
                x,y=k
                if img_thresh[(j_s[1]+y),(j_s[0]+x)]==0:
                    # check its 4 neigbors if any one of them is white then allow
                    count=0
                    new_point=(j_s[0]+x,j_s[1]+y)
                    for l in dir:
                        x1_,y1_=l
                        if img_thresh[(new_point[1]+y1_),(new_point[0]+x1_)]==255:
                            count+=1
                    if count==1:
                        niegbors_j.append((j_s[0]+x,j_s[1]+y))
            
        #     # make equation of line from i to j
            try:
                m=(j_s[1]-i[1])/(j_s[0]-i[0])
                c=j_s[1]-m*j_s[0]
                def f(x,y):
                    return y-m*x-c
            except:
                c=j_s[1]-m*j_s[0]
                def f(x,y):
                    return x-c
            # check if niegbors lie on same side
            count=0
            try:
                if f(*niegbors_i[0])*f(*niegbors_i[1])>=0:
                    count+=1
            except:
                count+=1
            try:
                if f(*niegbors_j[0])*f(*niegbors_j[1])>=0:
                    count+=1
            except:
                count+=1
            if count==2 or (count==1 and (i in endpoints_edge or j in endpoints_edge)):
                visibility_graph[i].append(j[0]) 
                visibility_graph[j[0]].append(i) 
                
                pygame.draw.line(screen,(0,0,255),(x1,y1),(x2,y2),5)
                pygame.display.flip()
    
        # # if vi is the beginning of an edge, E, not in S then Insert the E into S.
        # # increment alpha by a small amount 
        # j=(j,alpha)
        # pygame.time.wait(2000)
        alpha+=0.01
        # Far points at distance 1000 using this alpha connected with i
        new_half_line=((i[0],i[1]),(i[0]+10000*math.cos(alpha),i[1]+10000*math.sin(alpha)))
        # new_half_line=((i[0],i[1]),
        # draw half line
        #pygame.draw.line(screen,(0,0,255),(new_half_line[0][0],new_half_line[0][1]),(new_half_line[1][0],new_half_line[1][1]),1)
    #  print("Angle of half-line",math.atan2(new_half_line[1][1]-new_half_line[0][1],new_half_line[1][0]-new_half_line[0][0])*180/math.pi)
        pygame.display.flip()
        # check for all edges from B
        for j in edge_dic[j[0]]:
            X=i
            Y=new_half_line[1]
            C,D=j
            ex=[C,D]
            ex.sort()
            C,D=ex[0],ex[1]
            if not intersect(X,Y,C,D):
                # print("HERE")
                # if (C,D) in active_list:
                index_to_remove=-1
                for k in range(len(active_list)):
                    if active_list[k][0]==(C,D):
                        index_to_remove=k
                        break
                if index_to_remove!=-1:
                    active_list.pop(index_to_remove)
                    print("Removed",C,D)
            else:
                # print("NOTD")
                # if (C,D) not in active_list:
                check_index=-1
                for k in range(len(active_list)):
                    if active_list[k][0]==(C,D):
                        check_index=k
                        break
                if check_index==-1:
                    # check distance between i and line CD
                    # from i to intersection point on CD through half line
                    # find intersection point between line CD and half line
                    try:
                        m=(D[1]-C[1])/(D[0]-C[0])
                        c=C[1]-m*C[0]
                        r=abs(m*i[0]-i[1]+c)/math.sqrt(m**2+1)
                    except:
                        r=abs(i[0]-C[0])
                    # calculate distance from i to C
                    d1=math.sqrt((C[0]-i[0])**2+(C[1]-i[1])**2)
                    d2=math.sqrt((D[0]-i[0])**2+(D[1]-i[1])**2)
                    # move C towards D a bit
                    dx=D[0]-C[0]
                    dy=D[1]-C[1]
                    C_f=(C[0]+dx/1000,C[1]+dy/1000)
                # D_f=(D[0]-dx/1000,D[1]-dy/1000)
                    # check dist from i to C_f
                    d1_f=math.sqrt((C_f[0]-i[0])**2+(C_f[1]-i[1])**2)
                    d2_f=math.sqrt((D_f[0]-i[0])**2+(D_f[1]-i[1])**2)
                    if d1_f<d1 and d2_f<d2:
                        final=r
                    else:
                        final=min(d1,d2)
                    #final+=(d1+d2)/2
                    if r==0:
                        continue
                    active_list.append(((C,D),final))
                    print("Added",C,D,final)

# input()
        # wait for 2 sec
                active_list.sort(key=lambda x:x[1])
            #    pygame.time.wait(2000)

# use Djikstra to go from Source to Goal
Source=endpoints_edge[0]
Goal=endpoints_edge[1]

# make neighbors dictionary same as visibility_graph
neighbors=visibility_graph
path=[]
stack=[]
heapq.heappush(stack,(0,Source,[Source]))
visited=[]
found=0
print(visibility_graph)
while len(stack)>0:
    dis,current,path=heapq.heappop(stack)
    # Mark current
    # pygame.draw.circle(screen,(255,0,255),(current[0],current[1]),5)
    # pygame.display.flip()
    if current==Goal:
        found=1
        break
    if current in visited:
        continue
    visited.append(current)
    for neighbor in neighbors[current]:
        if neighbor[0] in visited:
            continue
        heapq.heappush(stack,(dis+math.sqrt((neighbor[0]-current[0])**2+(neighbor[1]-current[1])**2),neighbor,path+[neighbor]))




if found==0:
    print("No path found")
    x=input()
    exit()

# make all new_edges Blue
for edges in new_edges:
    pygame.draw.line(screen,(0,0,255),(edges[0][0],edges[0][1]),(edges[1][0],edges[1][1]),5)
    pygame.display.flip()

# Draw lines in path
for i in range(len(path)-1):
    pygame.draw.line(screen,(255,0,255),(path[i][0],path[i][1]),(path[i+1][0],path[i+1][1]),5)
    pygame.display.flip()


# go from source to goal




input()