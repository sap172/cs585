#this script launches all of the devices

#importing libraries
import os, subprocess,


def main(): 
    DEVICE_LIST = createDeviceList()
    for DEVICE in DEVICE_LIST:
        #start emulators
        startDevice(DEVICE)
        
def createDeviceList():
    #parse device list
    DELIM = "0.0.0.0"
    
    STR_LIST = {}
    STR_LIST = getGenyshellDevices().split(DELIM)[1:]
  
    DELIM = "|"
    DEVICE_LIST = []
    for line in STR_LIST:
        DEVICE_LIST.append(line.split(DELIM)[1][1:-6])
    return DEVICE_LIST
        
def startDevice(deviceName):
    print "Starting device: " + deviceName
    #start emulator
    SCRIPT = '"' + PATH + 'player" '
    PARAMS = '--vm-name "' + deviceName + '"'
    CMD = SCRIPT + PARAMS
    
    subprocess.Popen(CMD, shell=True)
    
if __name__ == '__main__':
    main()