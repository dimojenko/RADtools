# RADtools
various tools for use in the RAD Lab

___
## Utilities

### Attachment Downloader
This is a script for downloading attachments from Microsoft Outlook Inbox emails 
from the past day. If any files have the same name, they will have the end of their name
modified with a copy number to avoid overwriting. It is intended that this be used for 
downloading scanned test case data sheets. Once a series of data sheets have been scanned 
and emailed to the user, this script can be run to download those PDF files to the user's 
Downloads folder. Then the user could use the Rename PDF GUI in this repo to properly name 
the files. 

Since this script connects to Microsoft Outlook, it will need to be ran in a Microsoft shell, 
such as Windows Powershell.

### Rename PDF GUI
This is a Windows GUI for renaming scans of test case data sheets with the accepted naming scheme.
The user will be asked for a PDF file or multiple files to rename. The program then reads in 
those PDFs and extracts the test case number which is used to find the proper name for that
particular data sheet. Then the PDFs are renamed accordingly in their original location.

To use the Windows executable, the entire /renamePDFguiEXE/ folder will need to be downloaded. 
However, to run the program, only the executable (.exe) needs to be run or double-clicked. 
Alternatively, the Python scripts in /source/ can be used. There is one that only uses a terminal, 
and another for the GUI version. 

### Image Capture
This module contains functions used in capturing images from connected cameras. The image 
files are saved in the user's Camera Roll folder with the proper naming convention, and a resized 
image is displayed in a pop-up window when captured. This module is used in the IQTF Image 
Capture module as well as the Image Capture DOV within the DOV Assistant module in this repo.

___
## IQTF

### IQTF Image Capture
This module builds off of the Image Capture module in this repo, providing a GUI to more easily 
capture the required images for the IQTF tests. It allows users to choose a test to perform, 
either the Uniformity or Field of View test, and fill in metadata used to save the resulting 
images. To function as intended, this GUI will need to be ran on a Windows PC with no webcam, 
such that the scope has the only attached cameras. 

If running as a script, use a Microsoft shell.

There is also an standalone Windows executable version.

### IQTF Data Extractor
This is a script for extracting data from IQTF Uniformity and Field of View test results. It 
takes in image files which contain graphs and various test data and extracts the data relevant 
to that particular test's analysis. The results will then be printed to a shell. The 
data extraction is performed through an open source optical character recognition Python 
module. This script can also be used as a GUI if run with no arguments, and there is also a 
standalone Windows executable version.

___
## DOV

### DOV Assistant
This is a GUI intended for use with tests on the DOV test fixture. This GUI combines a widget 
from the ImageCapture module for capturing images and a toggled widget for moving a connected 
Zaber linear stage. The GUI allows the user to enter a scope name and trial number, select a 
test (either DOV or Color Accuracy), and enter a distance if applicable. Then when the 
"Capture Images" button is pressed, images are captured from the left and right eyes of the 
scope and saved with filenames according to the given metadata. All images will be saved in 
the user's Camera Roll folder. 

The zaberControl module provides the widget for directing the connected Zaber linear stage. 
To user inputs a COM port to connect to the device located there. Then the linear stage can 
be moved with buttons for quickly moving to the limits of motion or moved by input distances 
relative to the current position.

If using as a python script (not the executable), it will need to be ran in a Microsoft shell. 
Also if using as a script, the ImageCapture module will be necessary.

### DOV Analyzer
This is a GUI for assisting with the analysis of data from the DOV test results. This GUI allows
one to select a folder of DOV analysis CSVs, which are output from running the 4 captured DOV 
images through the Imatest analysis software. The code will then parse the CSVs for the 
relevant data, insert the data into the DOV calculator Excel document, and save a copy of the 
result. The Python script can be run with the argument as the path to a folder of DOV analysis 
CSVs, and can also be used as a GUI if run with no arguments. There is also an executable version.
