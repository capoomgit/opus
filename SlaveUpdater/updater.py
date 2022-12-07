import os
import sys
import shutil
import time
import subprocess

winStartup = os.getenv('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
clientFolder = os.getenv('LOCALAPPDATA') + '\\CapoomClient\\'

getClientPath = "P:\\pipeline\\standalone\\client\\"

def updateClient():
    time.sleep(1)

    # Remove pycache folder
    try:
        shutil.rmtree(clientFolder + '__pycache__')
    except:
        pass


    # Delete old client files except "updater.py"
    for file in os.listdir(clientFolder):
        if file != "updater.py":
            os.remove(clientFolder + file)

    # Sleep for 1 second to make sure the files are deleted
    time.sleep(1)

    # Copy files in clientFolder to getClientPath except "updater.py"
    for file in os.listdir(getClientPath):
        if file != 'updater.py':
            shutil.copy(getClientPath + file, clientFolder + file)

    #run startClient.bat then close self
    time.sleep(6)
    
    # os.system(clientFolder + 'startClient.bat')
    # Run startClient.bat as new process
    subprocess.Popen(clientFolder + 'startClient.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)

    # subprocess.Popen(clientFolder + 'startClient.bat', creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print("Client updated and started")
    sys.exit()
    
    return
    
    

            
        



if __name__ == '__main__':
    updateClient()
 