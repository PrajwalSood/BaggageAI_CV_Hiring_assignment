# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 19:40:46 2021

@author: prajw
"""
from utils import rotate, get_threat, get_bg, overlay_transparent
import sys
import cv2
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    
    ccw = False
    if len(sys.argv) == 5:
        ccw = True
            
    threat = cv2.imread(sys.argv[1])
    rgba = get_threat(threat, ccw = ccw)
    # threat = cv2.imread('threat_images/BAGGAGE_20170522_115645_80428_B.jpg')
    bg = cv2.imread(sys.argv[2])
    bg, x,y,w,h = get_bg(bg)
    f = 0
    c = 0
    while not f:
        try:
            if w>200 or h>150:
                w = 200
                h = 150
            out = overlay_transparent(bg, rgba, x, y, (w,h))
            plt.imshow(out)
            cv2.imwrite(sys.argv[3], out)
            f = 1
        except:
            c+=1
            if c>1000:
                print('Max Tries Exceeded, check input image dimensions and try again')
                break
    
