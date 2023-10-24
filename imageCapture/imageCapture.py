#!/usr/bin/python3
""" Image Capture

This module provides functions to capture images and save them in the user's 
Camera Roll folder. The images are also displayed and a notification 
message is returned.
CaptureImage must be run in a Windows shell.

Author: Dimitri Mojsejenko
"""
import cv2
import subprocess
from os.path import isfile
import ctypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def resizeImage(image, width=None, height=None):
    """Resizes an image based on given height or width."""
    dim = None # dim tuple passed to cv2.resize needs to be (width, height)
    (h, w) = image.shape[:2]
    if width is None:
        if height is None:
            return image
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def captureImage(camNum, fname, fcomp=[cv2.IMWRITE_JPEG_QUALITY, 90], webcam=True):
    """Captures an image from a selected camera.
    
    Parameters
    ~~~~~~~~~~
    camNum : int
        The index of the camera; starts at 0.
    fname : str
        The filename to save the image as.
    fcomp : list, optional
        The image compression settings.
    webcam: bool, optional
        True when webcam is connected.

    Returns
    ~~~~~~~
    msgText : str
        The notification message text.

    """
    # get the path to the user's Camera Roll folder
    if webcam: # laptop
        user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        cameraRoll = "C:\\Users\\" + user + "\\OneDrive - JNJ\\Pictures\\Camera Roll\\"
        # image window placement (laptop)
        x_left = 230
        x_right = 1190
        y = 220
        # adjust camNum to skip index of webcam (0)
        camNum = camNum + 1
    else: # no webcam == PC
        cameraRoll = "C:\\Users\\User\\Pictures\\Camera Roll\\"
        # image window placement (PC)
        x_left = 90
        x_right = 690
    fpath = cameraRoll + fname
    
    # capture image
    cam = cv2.VideoCapture(camNum, cv2.CAP_DSHOW)

    # resize from default 640x480 to 1920x1080
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    result, image = cam.read()
    msgText = ''
    if result:
        # check if file already exists
        resp = 1
        if isfile(fpath):
            fileMsg = "File already exists at: \n"+fpath+"\n\nOkay to overwrite?"
            resp = ctypes.windll.user32.MessageBoxW(0, fileMsg, "File Check", 1)
        if not resp == 2: # 2 = cancel
            # default JPG quality of Windows Camera App is around 90
            cv2.imwrite(fpath, image, fcomp)
            
            # resize displayed image
            imageResized = resizeImage(image, width=500) # width=500 height=281
            
            # display image and move window
            #  - moves are based on screen and window sizes
            #    - laptop screen size: width=1280 height=720
            #    - PC screen size: width=1920 height=1080
            cv2.namedWindow(fname)

            if camNum == 2 or (not webcam and camNum == 1): # left eye
                cv2.moveWindow(fname, x_left, y)
            else: # right eye
                cv2.moveWindow(fname, x_right, y)
            cv2.imshow(fname, imageResized)
            msgText = "Image saved: " + fname + '\n'
    else:
        msgText = "Failed to capture image.\n"
    return msgText