#!/usr/bin/python3
""" Image Capture

This program is to be used with the DOV tests to capture the required
images and save them in the proper format. The files will be saved in 
the user's Camera Roll folder.

Author: Dimitri Mojsejenko
"""
import cv2
import subprocess
from tkinter import *

# camera 0 = webcam
# camera 1 = right eye of scope
# camera 2 = left eye of scope
    
def captureImage(camNum, fname):
    """Captures an image from a selected camera.
    
    Parameters
    ~~~~~~~~~~
    camNum : int
        The index of the camera; starts at 0.
    fname : str
        The filename to save the image as.
        
    Returns
    ~~~~~~~
    msgText : str
        The notification message text.
        
    """
    # get the path to the user's Camera Roll folder
    user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    cameraRoll = "C:\\Users\\" + user + "\\OneDrive - JNJ\\Pictures\\Camera Roll\\"
    fpath = cameraRoll + fname
    cam = cv2.VideoCapture(camNum, cv2.CAP_DSHOW)

    # resize from default 640x480 to 1920x1080
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    result, image = cam.read()
    msgText = ''
    if result:
        # default JPG quality of Windows webcam is around 90
        cv2.imwrite(fpath, image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        
        # resize displayed image
        imageResized = resizeImage(image, width=500) # width=500 height=281
        
        # display image and move window
        #  - moves are based on screen and window sizes
        #    - laptop screen size: width=1280 height=720
        cv2.namedWindow(fname)
        if camNum == 2: # left eye
            cv2.moveWindow(fname, 90, 220) # x, y
        elif camNum == 1: # right eye
            cv2.moveWindow(fname, 690, 220)
        else: # webcam or other
            cv2.moveWindow(fname, 140, 220)
        cv2.imshow(fname, imageResized)       
        msgText = "Image saved: " + fname + '\n'
    else:
        msgText = "Failed to capture image.\n"
    return msgText
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkVars():
    """Checks the given values in the Entry fields."""
    scopeEntry = scope.get()
    trialEntry = trial.get()
    msgText = ''
    if not scopeEntry:
        msgText += "Scope name was not provided.\n"
    if not trialEntry:
        msgText += "Trial number was not provided.\n"
    messageText.set(msgText)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def runTest():
    """Runs the selected test."""
    checkVars()
    if chosenTest.get() == "Color Accuracy":
        capImageColorAcc()
    else:
        capImageDOV()
    # keep images displayed till any key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
def capImageDOV():
    """Captures images for Direction of View test."""
    # 2 images total: 35mm or 50mm for left/
    name = ''
    if scope.get():
        name = str(scope.get()) + "_"
    name += "dov_" + str(chosenDist.get()) + "_"
    if trial.get():
        name += "trial" + str(trial.get()) + "_"
    msgText = messageText.get()
    for cam in range(1, 3):
        if cam == 1:
            rname = name + "right.jpg"
            msgText += captureImage(cam, rname)
        else:
            lname = name + "left.jpg"
            msgText += captureImage(cam, lname)
    messageText.set(msgText)

    #DEBUGGING:
    #msgText = captureImage(0, "test.jpg")
    #messageText.set(msgText)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def capImageColorAcc():
    """Captures images for Color Accuracy test."""
    # 2 images total: 50mm left/right
    name = ''
    if scope.get():
        name = str(scope.get()) + "_"
    name += "colorAcc_"
    if trial.get():
        name += "trial" + str(trial.get()) + "_"
    msgText = messageText.get()
    for cam in range(1, 3):
        if cam == 1:
            rname = name + "right.jpg"
            captureImage(cam, rname)
            msgText += captureImage(cam, rname)
        else:
            lname = name + "left.jpg"
            captureImage(cam, lname)
            msgText += captureImage(cam, lname)
    messageText.set(msgText)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def testCallback(*args):
    """Shows/hides the Distance Choice based on Test selection."""
    if chosenTest.get() == "Direction of View":
        row4.pack()
    else:
        row4.pack_forget()
        
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
# Main GUI loop

# create Tkinter GUI
root = Tk()
# get screen width and height
#  - 1280x720 for laptop
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
# set GUI window width and height
w = 400
h = 250
# set GUI window location to center of screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
root.title("Image Capture GUI")
     
# Scope Name
row1 = Frame(root)
lab1 = Label(row1, text="Scope Name: ")
scope = Entry(row1)
lab1.pack(side=LEFT, padx=2)
scope.pack(side=LEFT, expand=YES, fill=X)
row1.pack(side=TOP, fill=X, padx=5, pady=5)

# Trial Number
row2 = Frame(root)
lab2 = Label(row2, text="Trial Number: ")
trial = Entry(row2, width=7)
lab2.pack(side=LEFT, padx=2)
trial.pack(side=RIGHT)
row2.pack(side=TOP, padx=5, pady=5)

# Test Selection
row3 = Frame(root)
lab3 = Label(row3, text="Select test: ")
tests = ["Color Accuracy", "Direction of View"]
chosenTest = StringVar(root)
chosenTest.set("Color Accuracy")
chosenTest.trace("w", testCallback)
testChoice = OptionMenu(row3, chosenTest, *tests)
lab3.pack(side=LEFT, padx=3)
testChoice.pack(side=RIGHT)
row3.pack()

# Distance Choice
row4 = Frame(root)
lab4 = Label(row4, text="Distance to target:")
distances = ["35mm", "50mm"]
chosenDist = StringVar(root)
chosenDist.set("35mm")
distChoice = OptionMenu(row4, chosenDist, *distances)
lab4.pack(side=LEFT, padx=3)
distChoice.pack(side=RIGHT)

# Message
messageText = StringVar(root)
message = Label(root, textvariable=messageText)
message.pack(side=BOTTOM, pady=2)

# Capture Images
row5 = Frame(root)
capBut = Button(row5, text="Capture images")
capBut.bind('<Button>', lambda capButHandler: runTest())
capBut.pack()
row5.pack(side=BOTTOM, padx=5, pady=5)

root.mainloop()