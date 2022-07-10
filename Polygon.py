from collections import deque
import cv2
import numpy as np
import pygame
import heapq
import math

img=cv2.imread('House2.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)

# use 2 points
ps2=True

# copy of image thresh
img_thresh=thresh.copy()
# draw 20*20 grid on image and if any pixel in it is black then it is an obstacle
# for i in range(0,img.shape[0],10):
#     for j in range(0,img.shape[1],10):
#         # see if any pixel in it is black
#         flag=1
#         for k in range(i,i+10):
#             if k>=img.shape[0]:
#                 break
#             for l in range(j,j+10):
#                 if l>=img.shape[1]:
#                     break
#            #     print(k,l,i,j)
#                 if thresh[k,l]==0:
#                     # draw 20*20 grid on image
#                     cv2.rectangle(img_thresh,(j,i),(j+10,i+10),(0,0,0),-1)
#                     flag=0
#                     break
#             if flag==0:
#                 break
cv2.imwrite('House2_thresh.png',img_thresh)

# # # use erosion on the thresh
# kernel=np.ones((5,5),np.uint8)
# thresh=cv2.erode(thresh,kernel,iterations=3)
# #save it
# cv2.imwrite('House2_thresh.png',thresh)

# use shi-tomasi corner detection to find corners
# Shi-Tomasi algorithm
pygame.init()
screen=pygame.display.set_mode((img.shape[1],img.shape[0]))
screen.blit(pygame.image.load('House2_thresh.png'),(0,0))
pygame.display.flip()


corners=cv2.goodFeaturesToTrack(img_thresh,1000,0.01,10) # image, max number of corners, quality level, min distance between corners
corners=np.int0(corners)
# draw corners on img_thresh
vis={}
print(corners)
input()
for i in range(len(corners)):
    x,y=corners[i].ravel()
    # bfs till you find an obstacle and make that a corner
    queue=deque([(x,y)])
    corners[i]=(x,y)
   # print("SPec",x,y)
    while len(queue)>0:
        x,y=queue.popleft()
        pygame.draw.circle(screen,(255,0,255),(x,y),1)
        pygame.display.flip()
        print(x,y)
        #input()
        vis[(x,y)]=1
        # end condition, among all 4 neigbors 2 should be 255
        count=0
        flag=0
        for l,s in [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]:
            if s>img.shape[0] or l>img.shape[1] or s<0 or l<0:
                continue
            #print(l,s,"what")

            if img_thresh[s,l]==255:
                count+=1
        print(count,"count",thresh[y,x])
        if count==1 or count==5:
            if thresh[y,x]==0:
                flag=1
        if flag:
            corners[i]=(x,y)
            break
        for p,q in [[1,0],[0,1],[-1,0],[0,-1]]:
            if (x+p,y+q) in vis:
                continue
            if x+p>img.shape[1] or y+q>img.shape[0] or x+p<0 or y+q<0:
                    continue
          #  print(p,q,"WD")
            vis[(x+p,y+q)]=1
            queue.append((x+p,y+q))
        # wait for .1 sec
    #    pygame.time.delay(100)
    pygame.draw.circle(screen,(0,0,255),(x,y),3)
    pygame.display.flip()
    #cv2.circle(img_thresh,(x,y),3,200,-1) 
# save it
print(len(corners),"HEY HERE PAUSE")
cv2.imwrite('House2_corners.png',img_thresh)

# import thresh in pygame



def is_obstacle_2(start,end):    # TODO: Use sweep and prune algorithm here
   # print(start[1],end[0])
    # if img_thresh[start[1],start[0]]==0:
    #         return True
    # if img_thresh[end[1],end[0]]==0:
    #     return True
    o_start=start[:]
    o_end=end[:]

    qu=[(start,end)]
    while len(qu)>0:
        start,end=heapq.heappop(qu) 
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            continue
        mid=(start[0]+end[0])//2,(start[1]+end[1])//2
        if img_thresh[mid[1],mid[0]]==0:
            # if distance from o_start or o_end is close to 3 pixels then it is not an obstacle
            # Check if this mid is 
            if abs(o_start[0]-mid[0])+abs(o_start[1]-mid[1])<=40 or abs(o_end[0]-mid[0])+abs(o_end[1]-mid[1])<=40:
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

# find edges for every neighbour of a corner
def find_edges(corner):
    # look in all 4 directions, 2 where there are obstacles, join them from the corner
    dir=[[1,0],[0,1],[-1,0],[0,-1]]
    edges_points=[]
    for i,j in dir:
       # print(img_thresh[corner[1]+i,corner[0]+j])
        if img_thresh[corner[1]+i,corner[0]+j]==0:
            # check all 4 neighbors near this point, only 1 of them is a 255
            flag=0
            for k,l in [[1,0],[0,1],[-1,0],[0,-1]]:
                if img_thresh[corner[1]+i+k,corner[0]+j+l]==255:
                  #  edges_points.append((corner[0]+j,corner[1]+i))
                    flag=1
                    break
            if flag:
                edges_points.append((corner[0]+j,corner[1]+i))
    if corner==(769,469):
        print("HELLO",edges_points)
        print(img_thresh[469,769])
        print(img_thresh[469,770])
        print(img_thresh[470,769])
        
        
    return edges_points

# find edges for every corner
edge_dic={}
for i in corners:
    x,y=i.ravel()
    #cv2.circle(img_thresh,(x,y),3,200,-1) 
   # print(img_thresh[y,x],"C")
    edges_points=find_edges((x,y))
    # join corners to edges
   # print(i,edges_points)
    edge_dic[(x,y)]=edges_points
    for j in edges_points:
        pygame.draw.line(screen,(255,0,0),(x,y),j,2)
        pygame.display.flip()
#input()
# find all edges in img_thresh
# for i in corners:
#     x,y=i.ravel()
#     # since every vertice has only 2 edges
#     maxi_edge=2
#     for j in corners:
#         x1,y1=j.ravel()
#         if (x,y)==(x1,y1):
#             continue
        
#         if is_not_obstacle((x,y),(x1,y1)):
#             maxi_edge-=1
#             pygame.draw.line(screen,(255,0,0),(x,y),(x1,y1),3)
#             pygame.display.flip()
#         if maxi_edge==0:
#             break

edges_full=[]
print(corners)
Coroners=[]
# all corners in list
for i in corners:
    x,y=i.ravel()
    Coroners.append((x,y))
for i in corners:
    x,y=i.ravel()
    # travel in direction of edge_dic till you find a corner
    # if you find a corner then add it to edges_full
    first=edge_dic[(x,y)]
    direction=(first[0][0]-x,first[0][1]-y)
    # travel in this direction
    print(direction)
    qu=[(x+direction[0],y+direction[1])]
    while len(qu)>0:
        x,y=heapq.heappop(qu)
        # draw the point
        pygame.draw.circle(screen,(0,0,255),(x,y),3)
        pygame.display.flip()
        # if x,y in corners
        if (x,y) in Coroners:
            p,q=i.ravel()
            edges_full.append(((x,y),(p,q)))
            # draw line
            pygame.draw.line(screen,(255,0,0),(x,y),(p,q),3)
            pygame.display.flip()
            print("LOa")
            break
        else:
            heapq.heappush(qu,(x+direction[0],y+direction[1]))
    


# join every corner with every other corner if is_obstacle_2 returns false and see if all neighbors from edge_dic fall on the same side of the line joining them
def line(p1,p2):
    # equation of line y=mx+c
    m=(p2[1]-p1[1])/(p2[0]-p1[0])
    c=p1[1]-m*p1[0]
    edge_points_1=edge_dic[p1]
    edge_points_2=edge_dic[p2]
    # use equation of line on points edge_points and see if they are both positive or negative
    vals_1=[]
    for val in edge_points_1:
        vals_1.append(m*val[0]+c-val[1])
        if vals_1[-1]>0:
            vals_1[-1]=1
        else:
            vals_1[-1]=-1
    vals_2=[]
    for val in edge_points_2:
        vals_2.append(m*val[0]+c-val[1])
        if vals_2[-1]>0:
            vals_2[-1]=1
        else:
            vals_2[-1]=-1
    # if positive, 1, if negative, -1
   # print(vals_1,vals_2)
    if vals_1[0]==vals_1[1] and vals_2[0]==vals_2[1]:
        print("BETE")
        return True
    return False


# select two points on screen
if ps2==True:
    running = True
    endpoints=[]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                endpoints.append(pos)
                pygame.draw.circle(screen,(255,0,0),pos,2)
                pygame.display.flip()
                if len(endpoints)==2:
                    running=False

    #find nearest corner to endpoints and make them green
    mini1=float('inf')
    mini2=float('inf')
    for i in corners:
        x,y=i.ravel()
        dist1=abs(x-endpoints[0][0])+abs(y-endpoints[0][1])
        dist2=abs(x-endpoints[1][0])+abs(y-endpoints[1][1])
        if dist1<mini1:
            mini1=dist1
            mini1_corner=i
        if dist2<mini2:
            mini2=dist2
            mini2_corner=i

    # make them green
    corner1=mini1_corner.ravel()
    corner2=mini2_corner.ravel()
    pygame.draw.circle(screen,(0,255,0),corner1,2)
    pygame.draw.circle(screen,(0,255,0),corner2,2)
    pygame.display.flip()
    # check on these 2 corners
    x1,y1=corner1
    x2,y2=corner2

    # print img_thresh of each 4 neighbours of corner1 and corner2
    print("COrner 1",corner1)

    for i in range(4):
        print(img_thresh[y1+i,x1])
    print("COrner 2",corner2)
    for i in range(4):
        print(img_thresh[y2+i,x2])


    if is_obstacle_2((x1,y1),(x2,y2)):
        print("NO")
        input()
    if line((x1,y1),(x2,y2)):
        print("YES")
        pygame.draw.line(screen,(255,0,0),corner1,corner2,2)
        pygame.display.flip()
        input()



else:

    for i in corners:
        i=i.ravel()
        x,y=i
        for j in corners:
            j=j.ravel()
            # print(i,j)
            x1,y1=j
            if x==x1 and y==y1:
                continue
            if x1>img.shape[1] or y1>img.shape[0]:
                continue
            if is_obstacle_2((x,y),(x1,y1)):
                continue
            if line((x,y),(x1,y1)):
                print("YES")
                pygame.draw.line(screen,(255,0,0),(x,y),(x1,y1),2)
                pygame.display.flip()
input()


