#!/usr/bin/python3
""" Image Capture DOV

This program is to be used with the DOV tests to capture the required
images and save them in the proper format. The files will be saved in 
the user's Camera Roll folder.

Author: Dimitri Mojsejenko
"""
import os
import sys
import cv2
import subprocess
from tkinter import *
imageCapturePath = os.path.join(os.path.dirname(__file__), '..', 'imageCapture')
sys.path.append(imageCapturePath)
from imageCapture import *

# camera 0 = webcam
# camera 1 = right eye of scope
# camera 2 = left eye of scope

class imageCaptureDOV(Frame):
    """Image Capture GUI"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        Frame.__init__(self, parent)
        # Scope Name
        row1 = Frame(self)
        lab1 = Label(row1, text="Scope Name: ")
        scope = Entry(row1)
        lab1.pack(side=LEFT, padx=2)
        scope.pack(side=LEFT, expand=YES, fill=X)
        row1.pack(side=TOP, fill=X, padx=5, pady=2)

        # Trial Number
        row2 = Frame(self)
        lab2 = Label(row2, text="Trial Number: ")
        trial = Entry(row2, width=7)
        lab2.pack(side=LEFT, padx=2)
        trial.pack(side=RIGHT)
        row2.pack(side=TOP, padx=5, pady=2)

        # Test Selection
        row3 = Frame(self)
        lab3 = Label(row3, text="Select test: ")
        tests = ["Color Accuracy", "Direction of View"]
        chosenTest = StringVar(self)
        chosenTest.set("Color Accuracy")
        chosenTest.trace("w", lambda *args: self.testCallback(parent, chosenTest.get(), row4))
        testChoice = OptionMenu(row3, chosenTest, *tests)
        lab3.pack(side=LEFT, padx=3)
        testChoice.pack(side=RIGHT)
        row3.pack()

        # Distance Choice
        row4 = Frame(self)
        lab4 = Label(row4, text="Distance to target:")
        distances = ["35mm", "50mm"]
        chosenDist = StringVar(self)
        chosenDist.set("35mm")
        distChoice = OptionMenu(row4, chosenDist, *distances)
        lab4.pack(side=LEFT, padx=3)
        distChoice.pack(side=RIGHT)

        # Message
        messageText = StringVar(self)
        message = Label(self, textvariable=messageText)
        message.pack(side=BOTTOM)

        # Capture Images
        row5 = Frame(self)
        capBut = Button(row5, text="Capture images", height=2, width=13)
        capBut.bind('<Button>', lambda capButHandler: self.runTest(chosenTest.get(), scope.get(), chosenDist.get(), trial.get(), messageText))
        capBut.pack()
        row5.pack(side=BOTTOM, padx=2, pady=2)

        self.pack(fill="both")
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def testCallback(self, parent, test, frame):
        """Shows/hides the Distance Choice based on Test selection."""
        if test == "Direction of View":
            frame.pack()
        else:
            frame.pack_forget()
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def checkVars(self, scope, trial, msg_text):
        """Checks the given values in the Entry fields."""
        msgText = ''
        if not scope:
            msgText += "Scope name was not provided.\n"
        if not trial:
            msgText += "Trial number was not provided.\n"
        msg_text.set(msgText)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def runTest(self, test, scope, dist, trial, msg_text):
        """Runs the selected test."""
        self.checkVars(scope, trial, msg_text)
        if test == "Color Accuracy":
            self.capImageColorAcc(scope, trial, msg_text)
        else:
            self.capImageDOV(scope, dist, trial, msg_text)
        # keep images displayed till any key press
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
    def capImageDOV(self, scope, dist, trial, msg_text):
        """Captures images for Direction of View test."""
        # 2 images total: 35mm or 50mm for left/right
        name = ''
        if scope:
            name = scope + "_"
        name += "dov_" + dist + "_"
        if trial:
            name += "trial" + trial + "_"
        msgText = msg_text.get()
        for cam in range(1, 3):
            if cam == 1:
                rname = name + "right.jpg"
                msgText += captureImage(cam, rname)
            else:
                lname = name + "left.jpg"
                msgText += captureImage(cam, lname)
        msg_text.set(msgText)

        #DEBUGGING:
        #msgText = captureImage(0, "test.jpg")
        #messageText.set(msgText)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def capImageColorAcc(self, scope, trial, msg_text):
        """Captures images for Color Accuracy test."""
        # 2 images total: 50mm left/right
        name = ''
        if scope:
            name = scope + "_"
        name += "colorAcc_"
        if trial:
            name += "trial" + trial + "_"
        msgText = msg_text.get()
        for cam in range(1, 3):
            if cam == 1:
                rname = name + "right.jpg"
                msgText += captureImage(cam, rname)
            else:
                lname = name + "left.jpg"
                msgText += captureImage(cam, lname)
        msg_text.set(msgText)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    root = Tk()
    imageCapFrame = Frame(root)
    imageCapGUI = imageCaptureDOV(imageCapFrame)
    imageCapFrame.pack(fill="both")
    # get screen width and height
    #  - 1280x720 for laptop
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # set GUI window width and height
    w = 350
    h = 250
    # set GUI window location to center of screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    root.title("Image Capture DOV GUI")
    root.mainloop()