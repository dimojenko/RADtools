#!/usr/bin/python3
""" DOV Analyzer

This script parses DOV analysis CSVs output from Imatest for relevant data, 
inserts the data into a copy of the DOV analysis Excel doc, and saves the resulting file.

* Requires that scope_dov_calc.xlsx exist in the same directory.

Author: Dimitri Mojsejenko
"""
import os
import sys
import glob
import argparse
import subprocess
import pandas as pd
import openpyxl as xl
from tkinter import *
from tkinter.filedialog import askdirectory
from math import *

class dovAnalyzerGUI(Frame):
    """DOV Analyzer GUI"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        Frame.__init__(self, parent)
        
        # Select DOV Analysis CSV files
        row1 = Frame(self)
        lab1 = Label(row1, text="Select folder of CSV files to extract DOV analysis data from:")
        lab1.pack(pady=5)
        row1.pack(side=TOP, fill=X, padx=5, pady=5)

        row2 = Frame(self)
        folder = Entry(row2)
        folderBut = Button(row2, text="Choose Folder", anchor='e')
        folderBut.bind('<Button>', lambda fButHandler: self._chooseFolder(folder))
        folder.pack(side=LEFT, expand=YES, fill=X)
        folderBut.pack(side=RIGHT)
        row2.pack(side=TOP, fill=X, padx=5, pady=5)

        # Extract Data
        row3 = Frame(self)
        extractBut = Button(row3, text="Extract Data and Analyze", height=2, width=20)
        extractBut.bind('<Button>', lambda capButHandler: analyzeDOVdriver(folder.get()))
        extractBut.pack()
        row3.pack(side=BOTTOM, padx=2, pady=4)

        self.pack(fill="both")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _chooseFolder(self, tkEntry):
        """Opens user dialogue asking for file, and stores name of file into given Tkinter entry."""
        # get the current user profile to start file dialogue at user's Downloads folder
        user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        if os.name == "nt":
            downloads = "C:\\Users\\" + user + "\\Downloads\\"
        else:
            downloads = "/mnt/c/Users/" + user + "Downloads/"
        fname = askdirectory(initialdir=downloads, title="Select folder", mustexist=True)
        tkEntry.delete(0,END)
        tkEntry.insert(0,fname)
     
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extractDOVdata(csv_path):
    """Given a path to a DOV analysis CSV, returns the relevant data.
    
    Parameters
    ~~~~~~~~~~
    csv_path : str
        The path of the DOV analysis CSV.
        
    Returns
    ~~~~~~~
    results : list
        A list of the 3 relevant data values, or 'nan' if not found.
    
    """
    # Saving CSVs in Excel changes row indexing by 2, possibly due to header/footer.
    dovCSV = pd.read_csv(csv_path, names=range(30)) 
    x_ind = 31
    y_ind = 32
    mag_ind = 36
    # Check if file saved in Excel, which changes y_coord to very long string.
    y_coord = dovCSV.iloc[y_ind,1]
    if len(y_coord) > 10:
        x_ind = x_ind + 2
        y_ind = y_ind + 2
        mag_ind = mag_ind + 2
        y_coord = dovCSV.iloc[y_ind,1]
    x_coord = dovCSV.iloc[x_ind,1]
    mag = dovCSV.iloc[mag_ind,2]
    results = [x_coord, y_coord, mag]
    return results

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calcDOVresults(dov_results, dov_calc_path, filename):
    """Given a list of extracted DOV data from all 4 CSVs and path to DOV calculator, save data in DOV calculator Excel doc.
    
    Parameters
    ~~~~~~~~~~
    dov_results : list
        The list of DOV results in order from running extractDOVdata.
        
    dov_calc_path: str 
        The path to the DOV calculator Excel document.
        
    filename: str
        The new name for the copy of the DOV calculator Excel document.
        
    Returns
    ~~~~~~~
    None : None
        Data saved in renamed copy of DOV calculator Excel doc in folder of CSVs.
    
    """
    dovCalc = xl.load_workbook(dov_calc_path)
    dataSheet = dovCalc["DOV"]
    left_35, right_35, left_50, right_50 = ([] for i in range(4))
    # Insert extracted DOV data into the DOV calculator Excel doc
    for row in dataSheet.iter_rows(min_row=5, max_row=6, min_col=2, max_col=7):
        resInd = 0
        for cell in row:
            if cell.row == 5:
                if cell.column < 5:
                    cell.value = dov_results[0][resInd]
                    left_35.append(dov_results[0][resInd])
                else:
                    cell.value = dov_results[1][resInd]
                    right_35.append(dov_results[1][resInd])
            else:
                if cell.column < 5:
                    cell.value = dov_results[2][resInd]
                    left_50.append(dov_results[2][resInd])
                else:
                    cell.value = dov_results[3][resInd]
                    right_50.append(dov_results[3][resInd])
            resInd = (resInd + 1) % 3
    
    dovCalc.save(filename)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("File saved: {}".format(filename))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    # Calculate and print final result
    B27 = float(left_35[0])*4/float(left_35[2])
    B28 = float(left_50[0])*4/float(left_50[2])
    C27 = float(left_35[1])*4/float(left_35[2])
    C28 = float(left_50[1])*4/float(left_50[2])   
    E27 = float(right_35[0])*4/float(right_35[2])
    E28 = float(right_50[0])*4/float(right_50[2])
    F27 = float(right_35[1])*4/float(right_35[2])
    F28 = float(right_50[1])*4/float(right_50[2])   
    B33 = atan((B28-B27+E28-E27)/(50-35))/pi*180
    C33 = atan((C28-C27+F28-F27)/(50-35)/2)/pi*180
    finalResult = asin(sqrt(sin(B33/180*pi)**2+sin(C33/180*pi)**2))/pi*180
    print("DOV Error (degrees): {:.5f}\n".format(finalResult))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def analyzeDOVdriver(dov_folder):
    """Given a folder of DOV analysis CSVs, extract data and run DOV analysis.
    
    Parameters
    ~~~~~~~~~~
    dov_folder: str
        A folder of DOV analysis CSVs.
        
    Returns
    ~~~~~~~
    None : None
        Data saved in renamed copy of DOV calculator Excel doc in given folder.
    
    """
    dovCalcPath = "./scope_dov_calc.xlsx"
    results = []
    
    # Modify path based on OS
    dov_folder = os.path.abspath(dov_folder)
    
    # Change path separator based on OS
    if os.name == "nt": # Windows
        sep = '\\'
    else:
        sep = '/'
    # last '/' or '\' not included when run with GUI
    if not dov_folder[-1] == sep:
        dov_folder = dov_folder + sep
    
    # Gather CSVs found in given folder
    csvList = glob.glob(dov_folder+"*.csv")
    
    # Check that DOV folder contains proper number of DOV analysis CSV files
    filesGood = True
    test, operator, scope, trial = ([] for i in range(4))
    filenameParts = [test, operator, scope, trial]
    print("The following CSVs were found:")
    for csv in csvList:
        print(csv)
        # Gather file metadata
        fileSplit = csv.split(sep)
        fileLoc = sep.join(fileSplit[:-1])
        filename = fileSplit[-1].split('_')
        test.append(filename[0])
        operator.append(filename[1])
        scope.append(filename[2])
        trial.append(filename[5])
        
    # Check that each file has the same test, operator, scope, and trial
    for part in filenameParts:
        if not [part[0]]*len(part) == part:
            filesGood = False

    # Assemble new filename
    newFileName = fileLoc+sep+"scope_dov_calc_"+operator[0]+'_'+scope[0]+'_'+trial[0]+".xlsx"

    if len(csvList) < 4:
        print("Only {} CSV files found. Check results folder and retry.".format(len(csvList)))
    else:
        if filesGood:
            for csv in csvList:
                results.append(extractDOVdata(csv))
            if results:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Extracted results:")
                print(results)
            calcDOVresults(results, dovCalcPath, newFileName)
        else:
            print("Files contain mismatching metadata. Check files and retry.")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "DOVresultsPath",
        nargs='?',
        type=str,
        help="The path to the folder of CSVs to extract data from"
    )
    args = argParser.parse_args()

    # check if intended as stand-alone command or interactive GUI (no args)
    if args.DOVresultsPath:
        # check that the given path is a directory
        if os.path.isdir(args.DOVresultsPath):
            analyzeDOVdriver(args.DOVresultsPath)
        else:
            print("The given path is not a directory. Retry with a folder of DOV results CSVs.")             
    else:
        #GUI
        root = Tk()
        dovAnaFrame = Frame(root)
        dovAnaGUI = dovAnalyzerGUI(dovAnaFrame)
        dovAnaFrame.pack(fill="both")
        # get screen width and height
        #  - 1280x720 for laptop
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # set GUI window width and height
        w = 500
        h = 200
        # set GUI window location to center of screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
        root.title("DOV Analyzer GUI")
        root.mainloop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()