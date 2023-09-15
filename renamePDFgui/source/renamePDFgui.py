#!/usr/bin/python3
"""PDF Renamer GUI

This script allows the user to rename a PDF or all PDFs within a folder according to the
test case code found within the PDF. Files that aren't PDFs or PDFs that aren't test
cases will not be modified.

Requires:
    * the following files to be in the runpath of renamePDFgui.py:
        * renamePDF.py
        * dataSheetTitles.txt
Author: Dimitri Mojsejenko
"""

import os
import subprocess
import glob
from tkinter import *
from tkinter.filedialog import askopenfilename
from renamePDF import *

def _renamePDF():
    # Check that given life number is an integer
    lifeNum = lifeNumEnt.get()
    try:
        lifeNum = int(lifeNum)
    except:
        message.configure(text="Please enter an integer value for test life number.")
    if isinstance(lifeNum, int):
        pdf_path, newTitle, lifeNum = _gatherVars()
        lifeNum = int(lifeNum)
        if len(pdf_path) > 1:
            print("Renaming multiple PDFs...")
            for f,t in zip(pdf_path, list(newTitle)):
                renamePDF(f, t, lifeNum)
            message.configure(text="All PDFs renamed.")
        else:
            print("Renaming PDF...")
            renamePDF(str(pdf_path[0]), str(newTitle[0]), lifeNum) #pdf_path and newTitle are lists here
            message.configure(text="PDF renamed.")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _gatherVars():        
    """Gathers and returns all the variables of the GUI to run _renamePDF()"""
    pdf_path = inFile.get()
    lifeNum = lifeNumEnt.get()
    newTitle = []
    if len(pdf_path) > 1:
        pdf_path = list(pdf_path.strip('}{').split('} {'))
        for f in pdf_path:
            newTitle.append(extract_title(f))
    else:
        newTitle = extract_title(pdf_path)
    return [pdf_path, newTitle, lifeNum]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _chooseFile(tkEntry):
    """Opens user dialogue asking for file, and stores name of file into given Tkinter entry"""
    # get the current user profile to start file dialogue at user's Downloads folder
    user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    downloads = "/mnt/c/Users/"+user+"/Downloads/"
    fname = askopenfilename(filetypes=[("PDF", ".pdf")], initialdir=downloads, title="Select PDF(s)", multiple=True)
    tkEntry.delete(0,END)
    tkEntry.insert(0,fname)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main GUI loop

# create Tkinter GUI
root = Tk()
root.geometry('600x250')
root.title("PDF Renamer GUI")

# first row
row1 = Frame(root)
lab1 = Label(row1, width=18, text="Select PDF(s) to rename:")
lab1.pack(pady=5)
row1.pack(side=TOP, fill=X, padx=5, pady=5)

# second row
row2 = Frame(root)
inFile = Entry(row2)
fileBut = Button(row2, text="Choose File(s)", anchor='e')
fileBut.bind('<Button>', lambda fButHandler: _chooseFile(inFile))
inFile.pack(side=LEFT, expand=YES, fill=X)
fileBut.pack(side=RIGHT)
row2.pack(side=TOP, fill=X, padx=5, pady=5)

# third row
row3 = Frame(root)
lab3 = Label(row3, text="Test Life Number")
#TODO: look into tkinter entry validation
lifeNumEnt = Entry(row3, width=5)
lifeNumEnt.pack(padx=5)
lab3.pack()
row3.pack(side=TOP, fill=X, padx=5, pady=5)

# rename PDF
mainBut = Button(root, text="Rename PDF(s)", anchor='n')
mainBut.bind('<Button>', lambda mainButHandler: _renamePDF())
mainBut.pack(side=TOP, padx=5, pady=5)

# message
message = Label(root, text="")
message.pack(side=BOTTOM, padx=5, pady=10)

root.mainloop()