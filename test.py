# test if 2 polygons intersect
# make 2 polygons on pygame
import pygame
import math
import random
import time
from shapely.geometry import Polygon
from poly import *
from line_segment import *


def check_intersection(endpoints_1,endpoints_2):
    # check for all edges1 with edges2 if any intersect
    edges1=[]
    for i in endpoints_1:
        edges1.append((i,endpoints_1[(endpoints_1.index(i)+1)%len(endpoints_1)]))
    edges2=[]
    for i in endpoints_2:
        edges2.append((i,endpoints_2[(endpoints_2.index(i)+1)%len(endpoints_2)]))
    # check intersection 
    for edge1 in edges1:
        for edge2 in edges2:
            if intersect(edge1[0],edge1[1],edge2[0],edge2[1]):
                return 1
    # check if any point of polygon1 is inside polygon2
    checker1=endpoints_1[0]
    checker2=endpoints_2[0]
    x_=polyx(endpoints_2,checker1)
    y_=polyx(endpoints_1,checker2)
   # print(x_,y_)
    if x_=="Inside" or y_=="Inside":
        return 2
    return 0

    