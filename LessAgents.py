import cv2
import numpy as np
import pygame
import heapq
from Agent import *
from test_3 import *
img=cv2.imread('Tunnel.png')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,127,255,0)
#save thresh image
cv2.imwrite('thresh.jpg',thresh)
pygame.init()
img=pygame.image.load('thresh.jpg')
screen=pygame.display.set_mode((img.get_width(),img.get_height()))
screen.blit(img,(0,0))
configuration_map=np.zeros((img.get_height(),img.get_width()),dtype=np.int)
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
# for i in range(img.get_width()):
#     for j in range(img.get_height()):
#         points=robot_config((i,j),5)
#         if points==False:
#             configuration_map[j,i]=0
#         else:
#             configuration_map[j,i]=255
#     cv2.imwrite('configuration_map_Tunnel.jpg',configuration_map)


configuration_map=cv2.imread('configuration_map_Tunnel.jpg')
gray=cv2.cvtColor(configuration_map,cv2.COLOR_BGR2GRAY)
ret,configuration_map=cv2.threshold(gray,127,255,0)
# make configuration map for radius r as a image
# check collision of a circle of r radius with black pixels

def manhattan_distance(start,end):
    return pow(abs(start[0]-end[0])**2+abs(start[1]-end[1])**2,0.5)
def is_obstacle_2(start,end):
    dx=end[0]-start[0]
    dy=end[1]-start[1]
    # print(start)
   # print(start,end)
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

n=2
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

# while True:
#    # screen.blit(img,(0,0))
#     for bot in bots:
#         if bot.path==[]:
#             while True:
#                 # new goal
#                 x=np.random.randint(0,img.get_width())
#                 y=np.random.randint(0,img.get_height())
#                 # check (x,y) in configuration_map
#                 if configuration_map[y,x]==255:
#                     bot.goal=(x,y)
#                     break
#             #pygame.draw.circle(screen,(255,255,0),agent.goal,5)
#             # A* from bot.pos to bot.goal
#             stack=[]
#             heapq.heappush(stack,(0,bot.pos))
#             visited=set()
#             visited.add(bot.pos)
#             box=3
#             # store all the possible directions in dx4
#             dx4=[]
#             for i in range(box):
#                 for j in range(box):
#                     if i-box//2==0 and j-box//2==0:
#                         continue
#                     dx4.append((i-box//2,j-box//2))
#                     #print(dx4)
#                     #dx4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
#                     heap=[]
#                     heapq.heappush(heap,(manhattan_distance(bot.pos,bot.goal),0,bot.pos,[bot.pos]))
#                     visited=set()
#                     found=-1
#             while heap:
#                 cost,path_cost,pos,path=heapq.heappop(heap)
#                 if pos==bot.goal:
#                     found=path_cost
#                     break
#                 if pos in visited:
#                     continue
#                 visited.add(pos)
#                 for dx,dy in dx4:
#                     new_pos=(pos[0]+dx,pos[1]+dy)
#                     if new_pos[0]<0 or new_pos[0]>=img.get_width() or new_pos[1]<0 or new_pos[1]>=img.get_height() or is_obstacle_2(pos,new_pos):
#                         continue
#                     if configuration_map[new_pos[1],new_pos[0]]==0:
#                         continue
#                     if new_pos in visited:
#                         continue
#                     new_cost=path_cost+manhattan_distance(pos,new_pos)
#                     heapq.heappush(heap,(manhattan_distance(new_pos,bot.goal),new_cost,new_pos,path+[new_pos]))
#             if found==-1:
#                 print('no path')
#                 bot.path=[]
#             bot.path=path[::-1]
#             bot.I=len(path)-1
#             # draw path
#             # for i in range(len(path)-1):
#             #     pygame.draw.line(screen,(0,0,255),path[i],path[i+1],1)
#             pygame.display.flip()
            
            
#         else:
#             # move bot
        #    print("A")
#             if bot.goal!=bot.path[0]:
#                 print("F")
#             pygame.draw.circle(screen,(255,255,0),bot.goal,5)
#             for i in range(0,bot.I,4):
#                 pygame.draw.line(screen,(255,0,0),bot.path[i],bot.path[i+1],1)
#             bot.pos=bot.path[bot.I-1]
#             bot.I-=1
#             if bot.I==0:
#                 bot.path=[]
#                 bot.I=0
#             # clear earlier bot from screen
#             pygame.draw.circle(screen,(255,255,255),bot.early,5)
#             pygame.draw.circle(screen,(0,0,0),bot.pos,5)
#             pygame.display.flip()
#             bot.early=bot.pos
            
    
while True:
       # screen.blit(img,(0,0))
    for bot in bots:
        if bot.path==[]:
            # pygame.draw.circle(screen,(255,255,255),bot.goal,5)
            bot.early=bot.goal
            while True:
                # new goal
                x=np.random.randint(0,img.get_width())
                y=np.random.randint(0,img.get_height())
                # check (x,y) in configuration_map
                if configuration_map[y,x]==255:
                    bot.goal=(x,y)
                    main_min=math.inf
                    minpoint=(0,0)
                    for polygon in Polygons:
                        minpoint=(0,0)
                        min_dist=math.inf
                        exes=[]
                        for i in range(len(polygon)):
                            exes.append((polygon[i],polygon[(i+1)%len(polygon)]))
                        # print(exes)
                        for edge in exes:
                            dist,neare=pnt2line(bot.goal,edge[0],edge[1])
                        # print(edge,endpoints)
                            if dist<min_dist:
                                minpoint=neare
                                min_dist=dist
                        if min_dist<main_min:
                            main_min=min_dist
                        # pygame.draw.circle(screen,(255,0,0),minpoint,5)
                    # pygame.draw.circle(screen,(255,255,0),bot.goal,5)
                    # pygame.display.flip()
                    if main_min<=70:
                   #     input()
                        continue
                #    print(min_dist)
                    break
           # pygame.draw.circle(screen,(255,255,0),bot.goal,5)
           # pygame.display.flip()
            # print("HAPpened")
      #      bot.path=["A"]
           # endpoints=[bot.pos,bot.goal]
            points_f=[]
            stack=[]
            heapq.heappush(stack,(0,bot.pos))
            visited=set()
            visited.add(bot.pos)
            box=3
            # store all the possible directions in dx4
            dx4=[]
       #     print(bot.pos,bot.goal,"AXVD")
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
            for i in range(0,bot.I,4):
                    bot.trajectory.append(bot.path[i])
            bot.trajectory.reverse()
            bot.trajectory.append(bot.goal)
       #     pygame.display.flip()
            
        else:
            # move bot
            oastin=(0,0)
            lastin=[]
           # print(bot.trajectory)
            for i in range(len(bot.trajectory)):
                lastin=bot.trajectory[i]
                lastin=(int(lastin[0]),int(lastin[1]))
                if is_obstacle_2((int(bot.pos[0]),int(bot.pos[1])),lastin)==False:
                    oastin=bot.trajectory[i]
                 #   pygame.draw.circle(screen,(255,0,0),oastin,8)
            # draw a circle on lastin
            oastin=(int(oastin[0]),int(oastin[1]))
            if oastin!=bot.lastseen:
                pygame.draw.circle(screen,(255,255,255),bot.lastseen,8)
                bot.lastseen=oastin
            pygame.draw.circle(screen,(255,0,0),oastin,8)
            #pygame.display.flip()
            if math.sqrt((bot.goal[0]-bot.pos[0])**2+(bot.goal[1]-bot.pos[1])**2)<=15:
                bot.pos=bot.goal
                pygame.draw.circle(screen,(255,255,255),bot.early,5)
                pygame.draw.circle(screen,(0,0,0),bot.pos,5)
                bot.trajectory=[]
          #      pygame.draw.circle(screen,(0,0,0),bot.goal,5)
                for i in range(0,bot.I,4):
                    pygame.draw.line(screen,(255,255,255),bot.path[i],bot.path[i+1],1)
             #   pygame.display.flip()
                bot.path=[]
                continue
            pygame.draw.circle(screen,(255,255,0),bot.goal,5)
            #pygame.draw.circle(screen,(0,0,0),bot.pos,5)
            for i in range(0,bot.I,4):
                pygame.draw.line(screen,(255,0,0),bot.path[i],bot.path[i+1],1)
          #  pygame.display.flip()
            for polygon in Polygons:
                minpoint=(0,0)
                min_dist=math.inf
                exes=[]
                for i in range(len(polygon)):
                    exes.append((polygon[i],polygon[(i+1)%len(polygon)]))
                # print(exes)
                for edge in exes:
                    dist,neare=pnt2line(bot.pos,edge[0],edge[1])
                # print(edge,endpoints)
                    if dist<min_dist:
                        minpoint=neare
                        min_dist=dist
                #    input()
               # print(min_dist)
                # pygame.draw.circle(screen,(255,0,0),minpoint,5)
                # pygame.display.flip()
                points_f.append(minpoint)
            box=[]
            for bo in bots:
                if bo==bot:
                    continue
                else:
                    box.append(bo.pos)
         #   print("BOX",box)
            forc=force(bot.pos,points_f,box)
            mag=math.sqrt(forc[0]**2+forc[1]**2)
         #   print("MAG",mag)
            # draw a arrow in the direction of force
            angle=math.atan2(forc[1],forc[0])
            # draw a arrow of size 10 in the direction of force
            # pygame.draw.line(screen,(255,0,0),bot.pos,(bot.pos[0]+10*math.cos(angle),bot.pos[1]+10*math.sin(angle)),2)
            # pygame.display.flip()
            # attract to goal
            forced=attractive_force(bot.pos,bot.lastseen,0.000003)
            maga=math.sqrt(forced[0]**2+forced[1]**2)
         #   print("MAG_ATT",maga)
            # draw a arrow in the direction of force
            angle=math.atan2(forced[1],forced[0])
            # draw a arrow of size 10 in the direction of force
            # pygame.draw.line(screen,(0,255,0),bot.pos,(bot.pos[0]+10*math.cos(angle),bot.pos[1]+10*math.sin(angle)),2)
            # pygame.display.flip()
            forc=[forced[0]+forc[0],forced[1]+forc[1]]
         #   print(forc)
            magx=math.sqrt(forc[0]**2+forc[1]**2)
       #     print("MAGX",magx)
            
            bot.pos=(bot.pos[0]+forc[0]/magx*10,bot.pos[1]+forc[1]/magx*10)
            #  clear earlier bot from screen
            pygame.draw.circle(screen,(255,255,255),bot.early,5)
            
            pygame.draw.circle(screen,(0,0,0),bot.pos,5)
            #pygame.display.flip()
            bot.early=bot.pos
            # wait for 1 sec sing pygame
           # pygame.time.wait(1)
            # draw polygons and fill them with color
            for poly in range(len(Polygons)):
                if poly==0:
                    pygame.draw.polygon(screen,(255,0,0),Polygons[poly],1)
                    continue
                polygon=Polygons[poly]
                pygame.draw.polygon(screen,(0,0,0),polygon)
    pygame.display.flip()
            # draw bot

            

input()