#!/usr/bin/python3
"""Email Attachment Downloader

This script allows one to download attachments from their Microsoft Outlook
Inbox. If any files have the same name, they will have the end of their name
modified with a number to avoid overwriting. The files will be saved in the 
user's Downloads folder.

Requirements:
    - needs to be run in Windows Powershell

Author: Dimitri Mojsejenko
"""
import os
import subprocess
from datetime import date
try:
    import win32com.client as win32
except:
    import pywin32 as win32
    
def attachDL():
    """Downloads attachments from Outlook emails received today"""
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # 6 is the code for the Inbox folder
    # get the path to the user's Downloads folder
    user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    downloads = "C:\\Users\\" + user + "\\Downloads\\" # need to use Windows style path
    # gather all the inbox messages
    messages = inbox.Items
    for message in messages:
        attachments = message.attachments
        sendDate = message.Senton.date()
        for attachment in attachments:
            # limit results to today's emails
            if sendDate == date.today():
                print(attachment.FileName)
                attachPath = downloads + attachment.Filename
                # check if duplicate filename already downloaded
                if os.path.isfile(attachPath):
                    print("File already downloaded. Renaming...")
                    copyNum = 0
                    while os.path.isfile(attachPath):
                        pathSplit = attachPath.split('.')
                        pathExt = pathSplit[-1:]
                        pathNoExt = pathSplit[:-1]
                        copyNum = copyNum + 1
                        if copyNum > 1:
                            pathSplit = attachPath.split('_')
                            attachPath = '_'.join(pathSplit[:-1]) + '_copy(' + str(copyNum) + ').' + pathExt[0]
                        else:
                            attachPath = pathNoExt[0] + '_copy(' + str(copyNum) + ').' + pathExt[0]
                attachment.SaveAsFile(attachPath)
                print("Downloaded: ", attachPath)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
if __name__ == '__main__':
    attachDL()