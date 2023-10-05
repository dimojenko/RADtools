# RADtools
various tools for use in the RAD Lab

## Rename PDF GUI
This is a Windows GUI for renaming scans of test case data sheets with the accepted naming scheme.
The user will be asked for a PDF file or multiple files to rename. The program then reads in 
those PDFs and extracts the test case number which is used to find the proper name for that
particular data sheet. Then the PDFs are renamed accordingly in their original location.

To use the Windows executable, the entire /renamePDFguiEXE/ folder will need to be downloaded. 
However, to run the program, only the executable (.exe) needs to be run or double-clicked. 
Alternatively, the Python scripts in /source/ can be used. There is one that only uses a terminal, 
and another for the GUI version. 

## Attachment Downloader
This is a script for downloading attachments from Microsoft Outlook Inbox emails 
from the past day. If any files have the same name, they will have the end of their name
modified with a copy number to avoid overwriting. It is intended that this be used for 
downloading scanned test case data sheets. Once a series of data sheets have been scanned 
and emailed to the user, this script can be run to download those PDF files to the user's 
Downloads folder. Then the user could use the Rename PDF GUI in this repo to properly name 
the files. 

Since this script connects to Microsoft Outlook, it will need to be run in a Microsoft shell, 
such as Windows Powershell.

## Image Capture
This module contains functions used in capturing images from connected cameras. The image 
files are saved in the user's Camera Roll folder and a resized image is displayed in a pop-up 
window when captured. There are also modules which can be imported or used as scripts to run 
the DOV or IQTF image captures with a GUI.

## DOV Assistant
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
