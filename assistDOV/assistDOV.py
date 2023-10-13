#!/usr/bin/python3
""" DOV Assistant

This program is to be used with the DOV tests to capture the required
images and save them in the proper format. The files will be saved in 
the user's Camera Roll folder. It connects to an attached camera to take 
images and allows the user to connect to a Zaber linear stage to move 
the target as necessary for the DOV tests. 

Author: Dimitri Mojsejenko
"""
import os
import sys
import cv2
import subprocess
from tkinter import *
from zaber.serial import AsciiSerial, AsciiDevice
imageCapturePath = os.path.join(os.path.dirname(__file__), '..', 'imageCapture')
sys.path.append(imageCapturePath)
from imageCaptureDOV import *
from zaberControl import *

def toggleFrame(rootTk, frame):
    """Shows/hides a frame based on toggle variable"""
    # set GUI window width and height
    w = 350
    if frame.winfo_viewable():
        frame.pack_forget()
        h = 270
    else:
        frame.pack(fill="both")
        h = 400        
    # get screen width and height
    #  - 1280x720 for laptop
    ws = rootTk.winfo_screenwidth()
    hs = rootTk.winfo_screenheight()   
    # set GUI window location to center of screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    rootTk.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    root = Tk()
    # Image Capture
    imageCapFrame = Frame(root)
    imageCaptureDOV(imageCapFrame)
    imageCapFrame.pack(fill="both")
    
    # Zaber Control
    zaberFrame = Frame(root)
    zaberGUI = zaberControl(zaberFrame)
    
    # Toggle Zaber Control
    zaberToggle = Button(root, text="Toggle Zaber Control")
    zaberToggle.bind('<Button>', lambda toggleHandler: toggleFrame(root, zaberFrame))
    zaberToggle.pack()
    
    # get screen width and height
    #  - 1280x720 for laptop
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # set GUI window width and height
    w = 350
    h = 270
    # set GUI window location to center of screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    
    root.title("DOV Assistant")
    root.mainloop()