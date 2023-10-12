#!/usr/bin/python3
""" PDF Renamer

This script renames PDF scans of data sheets to the proper name format.
The given files will be renamed in their original location.

Author: Dimitri Mojsejenko
"""
from PyPDF2 import PdfReader
import os
import sys
import argparse
import glob

def extract_title(pdf_path):
    """Given a path to a PDF, returns the title corresponding to the PDF test code
    
    Parameters
    ~~~~~~~~~~
    pdf_path : str
        The path of the PDF to rename
        
    Returns
    ~~~~~~~
    title : str
        The title of the test case in the PDF, or empty string if not found
    
    """
    # text file of data sheet titles with corresponding test code
    titles_txt = 'dataSheetTitles.txt'
    with open(pdf_path, 'rb') as f, open(titles_txt, 'r') as titles:
        pdf = PdfReader(f)
        pdf_info = pdf.metadata
        page = pdf.pages[0]
        print("PDF path: ", pdf_path)
        
        # Extract test code from page
        page_text = page.extract_text()
        testNum = ''
        try:
            # grab the first line of the page text
            line = page_text.split('\n')[1].strip()
            #testCode = testCode.split(':')[1].strip()
            words = line.split(' ')
            for word in words:
                word = word.strip(',')
                try:
                    if word[0:7] == "APO-TC-":
                        testNum = word[7::]
                        print("Test code extracted from PDF: ", word)
                except:
                    print("Error: could not extract test code from PDF.")
        except:
            print("Error: could not extract test code from PDF.")
        
        # Find corresponding title for test code
        title = ''
        if testNum:
            for line in titles:
                if testNum in line:
                    title = line.split(';')[1].strip()
        return title

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def renamePDF(pdf_path, title, lifeNum=''):
    """Renames a PDF to the given name based on the test code
    
    Parameters
    ~~~~~~~~~~
    pdf_path : str
        The path of the PDF to rename
    title : str
        The title of the test corresponding to the test code
    lifeNum : int, optional
        The test life number
        
    """
    if isinstance(lifeNum, int):
        lifeNum = 'T=' + str(lifeNum) + ' '
        
    pathSplit = pdf_path.split('/')[:-1]
    pathPrefix = '/'.join(pathSplit)
    newFilePath = pathPrefix + '/' + lifeNum + title + '.pdf'
    print("Renamed file: ", newFilePath)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    os.rename(pdf_path, newFilePath)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "PDFpath",
        type=str,
        help="The path to the PDF or folder of PDFs to rename"
    )
    argParser.add_argument(
        "-t", "--lifeNumber",
        nargs='?',
        type=int,
        help="The test life number to rename the PDF with"
    )
    args = argParser.parse_args()
    
    # Check if PDFpath is a single PDF or folder of PDFs
    if os.path.isdir(args.PDFpath):
        print("Given path is a directory.")
        pdfList = glob.glob(args.PDFpath+"*.pdf")
        print("The following PDFs were found:")
        for f in pdfList:
            print(f)
            
        choice = ''
        while not (choice == 'y' or choice == 'n'):
            choice = input("Would you like to rename them all? Enter 'y' to continue, and 'n' to quit:\n")
        if choice == 'n':
            sys.exit("Quitting script")
        else:
            for f in pdfList:
                newTitle = extract_title(f)
                if newTitle:
                    print("New title: ", newTitle)
                    renamePDF(f, newTitle, args.lifeNumber)
                    
    else: # single PDF to rename
        newTitle = extract_title(args.PDFpath)
        if newTitle:
            renamePDF(args.PDFpath, newTitle, args.lifeNumber)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()
