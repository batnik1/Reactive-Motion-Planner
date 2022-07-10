# draw a line from x1,y1 to x2,y2 in pygame
import pygame
import heapq
import numpy
from vectors import *
# draw a line in pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Path")
# blit white
screen.fill((255, 255, 255))
pygame.display.flip()

endpoints=[]
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            endpoints.append(event.pos)
            if len(endpoints)==2:
                running=False
endpoints1=endpoints[:]
running=True
endpoints=[]
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            endpoints.append(event.pos)
            if len(endpoints)==1:
                running=False

endpoints2=endpoints[:]

# draw a line 
# pygame.draw.line(screen,(0,0,255),endpoints1[0],endpoints1[1],1)
# # draw a point
# pygame.draw.circle(screen,(0,0,0),endpoints2[0],5)
# pygame.display.flip()


# find shortest distance of line from point

def pnt2line(pnt, start, end):
    # start,end=((21, 19), (21, 470))
    # pnt=(158, 246)
    # draw a line
    pygame.draw.line(screen,(0,0,255),start,end,1)
    pygame.draw.circle(screen,(0,0,0),pnt,5)
    pygame.display.flip()
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    # draw a point on nearest
    pygame.draw.circle(screen,(0,0,0),nearest,5)
    pygame.display.flip()
    return (dist, nearest)
print(pnt2line(endpoints2[0],endpoints1[0],endpoints1[1]))


input()