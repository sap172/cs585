#this file terminates all of the running emulators
#importing libraries
import os, subprocess

def main():

    if os.name is 'nt':
        stopDeviceWindows(DEVICE)
        
    #stop emulators
    if os.name is 'nt':
        killAllDevicesWindows()
        
def killAllDevicesWindows():
    #kills all device processes
    CMD = 'taskkill /IM player.exe'
    OUTPUT = subprocess.check_output(CMD)
    
def stopDeviceWindows(DEVICE):
    #stop emulator
    PROGRAM = 'player.exe'
    CMD = 'tasklist /v /fi "imagename eq ' + PROGRAM + '"'
        
    OUTPUT = subprocess.check_output(CMD)
    
    STR_LIST = OUTPUT.split(PROGRAM)
    
    for LINE in STR_LIST:
        if DEVICE[:-2] in LINE:
            PID = LINE.strip().split(" ")[0]
            
            #kill process
            CMD = 'taskkill /PID ' + PID
            OUTPUT = subprocess.check_output(CMD)
            
if __name__ == '__main__':
    main()