from numpy import ones,vstack
from numpy.linalg import lstsq

import cv2
import numpy as np
import pygame
import heapq
import math
import warnings
warnings.filterwarnings("ignore")

def hull(m,c,x,y):
    return y-m*x-c

def polyx(endpoints,checker):
    dealbreaker=0
    center=np.mean(endpoints,axis=0)
    for i in range(len(endpoints)):
        a,b=endpoints[i],endpoints[(i+1)%len(endpoints)]
        points = [a,b]
        x_coords, y_coords = zip(*points)
        A = vstack([x_coords,ones(len(x_coords))]).T
        m, c = lstsq(A, y_coords)[0]

        hout=hull(m,c,checker[0],checker[1])
        hin=hull(m,c,center[0],center[1])
        #print(hout,hin)
        if hout/hin<0:
            dealbreaker+=1

    if dealbreaker>0:
        return "Outside"
    else:
        return "Inside"

