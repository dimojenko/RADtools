#!/usr/bin/python3
""" Image Capture IQTF

This program is to be used with the IQTF tests to capture the required
images and save them in the proper format. The files will be saved in 
the user's Camera Roll folder.
This must be run in a Windows shell.

Author: Dimitri Mojsejenko
"""

from tkinter import *
from imageCapture import *

class imageCaptureIQTF(Frame):
    """Image Capture IQTF GUI"""
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

        # Run Number
        row2 = Frame(self)
        lab2 = Label(row2, text="Run Number: ")
        run = Entry(row2, width=7)
        lab2.pack(side=LEFT, padx=2)
        run.pack(side=RIGHT)
        row2.pack(side=TOP, padx=5, pady=2)

        # Test Selection
        row3 = Frame(self)
        lab3 = Label(row3, text="Select test: ")
        tests = ["Uniformity", "Field of View"]
        chosenTest = StringVar(self)
        chosenTest.set("Uniformity")
        testChoice = OptionMenu(row3, chosenTest, *tests)
        lab3.pack(side=LEFT, padx=3)
        testChoice.pack(side=RIGHT)
        row3.pack()
        
        # Save Image Type
        row4 = Frame(self)
        lab4 = Label(row4, text="Save image as: ")
        filetypes = ["jpg", "png (no compression)", "png (full compression)"]
        chosenFtype = StringVar(self)
        chosenFtype.set("jpg")
        fTypeChoice = OptionMenu(row4, chosenFtype, *filetypes)
        lab4.pack(side=LEFT, padx=3)
        fTypeChoice.pack(side=RIGHT)
        row4.pack()

        # Message
        messageText = StringVar(self)
        message = Label(self, textvariable=messageText)
        message.pack(side=BOTTOM)

        # Capture Images
        row5 = Frame(self)
        capBut = Button(row5, text="Capture images", height=2, width=13)
        capBut.bind('<Button>', lambda capButHandler: self.capImageIQTF(chosenTest.get(), scope.get(), run.get(), chosenFtype.get(), messageText))
        capBut.pack()
        row5.pack(side=BOTTOM, padx=2, pady=4)

        self.pack(fill="both")
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def checkVars(self, scope, run, msg_text):
        """Checks the given values in the Entry fields."""
        msgText = ''
        if not scope:
            msgText += "Scope name was not provided.\n"
        if not run:
            msgText += "Run number was not provided.\n"
        msg_text.set(msgText)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def capImageIQTF(self, test, scope, run, ftype, msg_text):
        """Captures images for selected test."""
        # 2 images total: left/right
        self.checkVars(scope, run, msg_text)
        if test == "Uniformity":
            name = "Uniformity_"
        else:
            name = "FOV_"
        if scope:
            name += scope + "_"
        if run:
            name += "Run" + run + "_"
        msgText = msg_text.get()
        
        match ftype:
            case "png (no compression)":
                fileExt = "png"
                fcomp = [int(cv2.IMWRITE_PNG_COMPRESSION),0]
            case "png (full compression)":
                fileExt = "png"
                fcomp = [int(cv2.IMWRITE_PNG_COMPRESSION),9]
            case _:
                fileExt = "jpg"
                fcomp = [cv2.IMWRITE_JPEG_QUALITY, 90]
        
        for cam in range(0, 2):
            if cam == 0:
                rname = name + "right." + fileExt
                msgText += captureImage(cam, rname, fcomp, webcam=True)
            else:
                lname = name + "left." + fileExt
                msgText += captureImage(cam, lname, fcomp, webcam=True)
        msg_text.set(msgText)
        # keep images displayed till any key press
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    root = Tk()
    imageCapFrame = Frame(root)
    imageCapGUI = imageCaptureIQTF(imageCapFrame)
    imageCapFrame.pack(fill="both")
    # get screen width and height
    #  - 1280x720 for laptop
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # set GUI window width and height
    w = 350
    h = 230
    # set GUI window location to center of screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    root.title("Image Capture IQTF GUI")
    root.mainloop()
