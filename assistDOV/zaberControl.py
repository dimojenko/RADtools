#!/usr/bin/python3
""" Zaber Controller

This program allows the user to control a Zaber device.

Author: Dimitri Mojsejenko
"""
from tkinter import *
from zaber.serial import AsciiSerial, AsciiDevice

class zaberControl(Frame):
    """Zaber Control GUI"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Connect Device
        #Frame.__init__(self, parent)
        row1 = Frame(self)
        comLabel = Label(row1, text="COM Port: ")
        comPort = StringVar()
        comPort.set("COM5")
        comBorder = Frame(row1)
        comEntry = Entry(comBorder, width=7, textvariable=comPort, bd=0)
        comBut = Button(row1, text="Connect")
        comBut.bind('<Button>', lambda comHandler: self.connectDevice(comPort.get(), messageText, comBorder))
        comLabel.pack(side=LEFT, padx=2)
        comBut.pack(side=RIGHT, padx=4)
        comBorder.pack(side=RIGHT, padx=2)
        comEntry.pack(padx=1, pady=1)
        row1.pack(side=TOP, padx=5, pady=5)
        
        # Movement Commands
        row2 = Frame(self)
        moveLabel = Label(row2, text="Relative Move (mm)")
        moveLabel.pack()
        row2.pack(side=TOP, pady=2)
        
        # Move Home
        row3 = Frame(self)
        homeBut = Button(row3, text="Home", width=7)
        homeBut.bind('<Button>', lambda homeHandler: self.homePosition(messageText))
        homeBut.pack(side=LEFT, padx=5)
        # Relative Move
        moveDist = StringVar()
        distEntry = Entry(row3, width=7, textvariable=moveDist)
        leftBut = Button(row3, text="Left", width=7)
        leftBut.bind('<Button>', lambda leftHandler: self.relativeMove(moveDist.get(), "left", messageText))
        rightBut = Button(row3, text="Right", width=7)
        rightBut.bind('<Button>', lambda rightHandler: self.relativeMove(moveDist.get(), "right", messageText))
        leftBut.pack(side=LEFT, padx=5)
        distEntry.pack(side=LEFT, padx=5)
        # Move to End
        endBut = Button(row3, text="End", width=7)
        endBut.bind('<Button>', lambda endHandler: self.endPosition(messageText))
        endBut.pack(side=RIGHT, padx=5)
        rightBut.pack(side=RIGHT, padx=5)
        row3.pack(side=TOP, padx=5, pady=2)
        
        # Message
        messageText = StringVar()
        message = Label(self, textvariable=messageText)
        message.pack(side=BOTTOM, pady=2)
        
        self.pack(fill="both")
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def connectDevice(self, com_port, msg_text, com_border):
        """Connect to device at given com_port and assign it to the global device."""
        try:
            port = AsciiSerial(com_port)
            global device
            device = AsciiDevice(port, 1)
            status = device.get_status()
            if not status == "BUSY" and not status == "IDLE":
                msg_text.set("No device found at "+com_port+". Check connection.")
                com_border.configure({"background": "red"})
            else:
                msg_text.set("Connected to device on "+com_port+".")
                com_border.configure({"background": "green"})
        except Exception as error:
            if type(error).__name__ == "SerialException":
                errorSplit = str(error).split(':')[1]
                errorDesc = errorSplit.split('(')[0].strip()
                if errorDesc == "PermissionError":
                    msg_text.set("Device already connected at "+com_port+".")
                    com_border.configure({"background": "green"})
                else:
                    msg_text.set("No device found at "+com_port+". Check connection.")
                    com_border.configure({"background": "red"})
            else:
                msg_text.set("No device found at "+com_port+". Check connection.")
                com_border.configure({"background": "red"})

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def homePosition(self, msg_text):
        """Home the device and check the result."""
        # home command is blocking and will run to completion
        reply = device.home() 
        if reply.reply_flag == "OK": # If command not accepted, received "RJ"
            msg_text.set("Device homed.")
        else:
            msg_text.set("Device home failed.")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def endPosition(self, msg_text):
        """Move device to the end of range of motion and check the result."""
        # move_abs command is blocking and will run to completion
        end = 1526940 # experimentally found to be end of ROM
        reply = device.move_abs(end)
        if reply.reply_flag == "OK":
            msg_text.set("Device at end position.")
        else:
            msg_text.set("Move device to end failed.")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def relativeMove(self, dist_mm, dir, msg_text):
        """Move device given distance (mm) in given direction and check the result."""
        # move_rel command is blocking and will run to completion
        if not dist_mm:
            dist_mm = "0"
        dist_f = float(dist_mm)
        dist = int(dist_f * 10000) # convert to microsteps: microstep ~= 10000 mm
        if dir == "left":
            dist = -dist
        reply = device.move_rel(dist)
        if reply.reply_flag == "OK":
            msg_text.set("Device moved to "+dir+" by approximately "+dist_mm+" mm.")
        else:
            msg_text.set("Device move failed.")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    root = Tk()
    zaberFrame = Frame(root)
    zaberGUI = zaberControl(zaberFrame)
    zaberFrame.pack(fill="both")
    # get screen width and height
    #  - 1280x720 for laptop
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # set GUI window width and height
    w = 350
    h = 170
    # set GUI window location to center of screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    root.title("Zaber Controller")
    root.mainloop()