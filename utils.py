# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 09:07:25 2021

@author: prajw
"""
import cv2
import numpy as np

def rotate(img, ccw = False):
    """Rotate the image to a new image .

    Args:
        img (np.ndarray of uint8): A numpy array of the image.
        ccw (bool, optional): Set to True to rotate image clockwise. Defaults to False.

    Returns:
        (np.ndarray of uint8): A numpy array of the image.
    """
    h, w = img.shape[:2]
    if ccw:
        return cv2.warpAffine(img, cv2.getRotationMatrix2D((w/2, h/2), 45, 0.7071), (w, h), borderValue = [255,255,255])
    else:
        return cv2.warpAffine(img, cv2.getRotationMatrix2D((w/2, h/2), -45, 0.7071), (w, h), borderValue = [255,255,255])

    

def get_threat(threat, ccw = False):
    """Get a color image from a given threat along with its alpha mask.

    Args:
        threat (np.ndarray of uint8): A numpy array of the 3 channel image.
        ccw (bool, optional): Set to True to rotate image clockwise. Defaults to False.

    Returns:
        (np.ndarray of uint8): A numpy array of the 4 channel image cropped to only include the rotated threat.
    """
    mask = np.where(cv2.cvtColor(threat, cv2.COLOR_BGR2GRAY) == 255, 0, 1).astype('uint8')

    
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    
    # Final threat image
    crop = threat[y:y+h,x:x+w]
    
    # plt.imshow(crop)
    
    rotated = rotate(crop, ccw = ccw)
    
    # plt.imshow(rotated)
    
    mask = np.where(cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY) >= 240, 0, 255).astype('uint8')
    # plt.imshow(mask)
    
    rgba = cv2.cvtColor(rotated, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask
    
    return rgba

def get_bg(bg):
    """Get a background color for a given background image .

    Args:
        bg (np.ndarray of uint8): A numpy array of the image.
    Returns:
        bg (np.ndarray of uint8): A numpy array of the image.
        x (int): The x coordinate of the top left of threat image.
        y (int): The y coordinate of the top left of threat image.
        w (int): The width of the threat image.
        h (int): The height of the threat image.
    """
    mask = np.where(cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY) == 255, 0, 1).astype('uint8')
    
    # plt.imshow(mask)
    
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = contours[-1]
    
    w = 0
    h = 0
    while w<50 or h<50: 
        index = sorted(np.random.choice(cnt.shape[0], 2, replace=False))  
        p = cnt[index][:,0,:]
        x,y,w,h = map(int , [p[0][0], p[0][1], abs(p[1][0] - p[0][0]), abs(p[1][1] - p[0][1])])
    
    return bg, x,y,w,h
    
# rgba = cv2.resize(rgba, (w,h))


def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
    """Overlay the image with transparent threat image withing the bag area.

    Args:
        background_img (np.ndarray of uint8): A numpy array of the image.
        img_to_overlay_t (np.ndarray of uint8): A numpy array of the image.
        x (int): topleft of the image
        y (int): topleft of the image
        overlay_size (1d List, optional): Desired overlay size. Defaults to None.

    Returns:
        bg_img (np.ndarray of uint8): A numpy array of the image with threat placed over the background
    """
    
    bg_img = background_img.copy()
	
    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    b,g,r,a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b,g,r))

    mask = cv2.medianBlur(a,5)

    h, w, _ = overlay_color.shape
    roi = bg_img[y:y+h, x:x+w]

    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))

    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

    bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

    return bg_img


