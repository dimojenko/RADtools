#!/usr/bin/python3
"""IQTF Data Fetcher

This script allows one to fetch the text data from a given image and 
filter out the desired data to document for the IQTF analysis. 

Author: Dimitri Mojsejenko
"""
import os
import glob
import subprocess
import argparse
from pytesseract import pytesseract # optical recognition
import cv2 # computer-vision library
import re # regular expressions
from tkinter import *
from tkinter.filedialog import askopenfilename

class getDataIQTF(Frame):
    """Data Extractor IQTF GUI"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        Frame.__init__(self, parent)
        
        # Select Images
        row1 = Frame(self)
        lab1 = Label(row1, text="Select images to extract IQTF data from:")
        lab1.pack(pady=5)
        row1.pack(side=TOP, fill=X, padx=5, pady=5)

        row2 = Frame(self)
        inFile = Entry(row2)
        fileBut = Button(row2, text="Choose File(s)", anchor='e')
        fileBut.bind('<Button>', lambda fButHandler: self._chooseFile(inFile))
        inFile.pack(side=LEFT, expand=YES, fill=X)
        fileBut.pack(side=RIGHT)
        row2.pack(side=TOP, fill=X, padx=5, pady=5)

        # Extract Data
        row3 = Frame(self)
        capBut = Button(row3, text="Extract Data", height=2, width=13)
        capBut.bind('<Button>', lambda capButHandler: self._extractIQTFdataGUI(inFile.get()))
        capBut.pack()
        row3.pack(side=BOTTOM, padx=2, pady=4)

        self.pack(fill="both")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _chooseFile(self, tkEntry):
        """Opens user dialogue asking for file, and stores name of file into given Tkinter entry"""
        # get the current user profile to start file dialogue at user's Pictures folder
        user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        if os.name == "nt":
            pictures = "C:\\Users\\" + user + "\\OneDrive - JNJ\\Pictures\\"
        else:
            pictures = "/mnt/c/Users/" + user + "/OneDrive - JNJ/Pictures/"
        fname = askopenfilename(filetypes=[("PNG", ".png"),("JPG", ".jpg")], initialdir=pictures, title="Select image(s)", multiple=True)
        tkEntry.delete(0,END)
        tkEntry.insert(0,fname)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _extractIQTFdataGUI(self, tkEntry):
        """Extracts IQTF data for given path to image or list of paths to images"""
        images = tkEntry.strip('{}').split('} {') # remove brackets added by file dialogue box
        results = []
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~ Extracting Data from Images ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for image in images:
            results.append(extractIQTFdata(image))
        # print results
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Extracted Data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for result in results:
            print(result)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extractIQTFdata(image_path):
    """Given a path to an image from an IQTF Uniformity/FoV test, returns the relevant data.
    
    Parameters
    ~~~~~~~~~~
    image_path : str
        The path of the image to extract data from.
        
    Returns
    ~~~~~~~
    result : str
        The result of the test, or empty string if not found.
    
    """

    # Open the image & store it in an image object.
    img = cv2.imread(image_path)
    # Resize image for better optical recognition
    #images = []
    #images.append(cv2.resize(img, None, fx=1.2, fy=1.2)) # cv2.INTER_LINEAR
    #images.append(cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC))
    #images.append(cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
    #images.append(cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_LANCZOS4))
    #images.append(cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4))
    image = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
    
    # Provide the tesseract executable location to pytesseract library (based on OS)
    if not os.name == "nt":
        pytesseract.tesseract_cmd = 'tesseract'
    else: # Windows
        pytesseract.tesseract_cmd = r"C:\Users\wmojseje\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    
    image_name = image_path.split('/')[-1].rstrip('.png')
    print(image_name)
    result = image_name+": "
    
    # Extract text from image
    image_text = pytesseract.image_to_string(image)
    
    # Split text into lines
    text_lines = image_text.split('\n')
    
    # Check which test the image is from
    if "Y (luminance) contours Normalized" in text_lines: # Uniformity
        print("IQTF Uniformity data found.")
        
        for line in text_lines:
            # Extract relevant data
            if "worst =" in line:
                index_L = line.index("(")
                index_R = line.index(")")
                result += line[index_L+1:index_R]
        
    elif "Lens Geometric Distortion" in text_lines[0]: # Field of View
        print("IQTF Field of View data found.")
        
        # regular expressions for data to extract
        thirdOrdCorner = re.compile("3.+LGD\s\(co")
        fovResult = re.compile(r"Field of View")
        
        for line in text_lines:
            if re.match(thirdOrdCorner, line):
                try:
                    result += line.split('=')[1].strip() + ", "
                except Exception as error:
                    print(error)
                    result += "error"
            elif re.match(fovResult, line):
                try:
                    result += line.split('=')[1].split()[0]
                except Exception as error:
                    print(error)
                    result += "error"
    else:
        result = ""
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")       
    return result
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "imagePath",
        nargs='?',
        type=str,
        help="The path to the image or folder of images to extract data from."
    )
    args = argParser.parse_args()
    
    result = []

    # check if intended as stand-alone command or interactive GUI (no args)
    if args.imagePath:
        # Check if imagePath is a single image or folder of images
        if os.path.isdir(args.imagePath):
            print("Given path is a directory.")
            imageList = glob.glob(args.imagePath+"*.png")
            print("The following images were found:")
            result = []
            for f in imageList:
                print(f)
                result.append(extractIQTFdata(f))
            for res in result:
                print(res)
        else: # single image
            result = extractIQTFdata(args.imagePath)
            print(result)
    else:
        # GUI
        root = Tk()
        iqtfFrame = Frame(root)
        iqtfGUI = getDataIQTF(iqtfFrame)
        iqtfFrame.pack(fill="both")
        # get screen width and height
        #  - 1280x720 for laptop
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # set GUI window width and height
        w = 400
        h = 200
        # set GUI window location to center of screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
        root.title("IQTF Data Extractor GUI")
        root.mainloop()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()    