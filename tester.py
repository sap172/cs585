import os, sys, subprocess, time
from multiprocessing import Process

PATH = 'C:\\Program Files\\Genymobile\\Genymotion\\'
#APK = 'C:\\Users\\parkin\\AndroidstudioProjects\\SimpleCalculator\\app\\build\\outputs\\apk\\app-debug.apk'
APK = 'app-debug.apk'
#TEST_APK = 'C:\\Users\\parkin\\AndroidstudioProjects\\SimpleCalculator\\app\\build\\outputs\\apk\\app-debug-test-unaligned.apk'
TEST_APK = 'app-debug-test-unaligned.apk'
PACKAGE = 'com.twooilyplumbers.simplecalculator'
TEST_PACKAGE = 'com.twooilyplumbers.simplecalculator.test'
TEST_RUNNER = 'android.test.InstrumentationTestRunner'
LOG_DIR = 'logs'
ADB_SCRIPT = 'adb -s '
DELAY = 60

def main(args):
    
    print APK
    
    DEVICE_LIST = createDeviceList()
    for DEVICE in DEVICE_LIST:
        #start emulators
        startDevice(DEVICE)
    
    time.sleep(DELAY)
    
    IP_MAP = getMapOfIPs()
          
    #for DEVICE in DEVICE_LIST:
    for IP in IP_MAP:
        print IP
        try:
            APK_EXISTS = findAPK(PACKAGE, IP)
            if APK_EXISTS:
                removeAPK(PACKAGE, IP)
                
            APK_EXISTS = findAPK(PACKAGE + '.test', IP)
            if APK_EXISTS:
                removeAPK(PACKAGE + '.test', IP)
            
            print "Installing APK..."
            installAPK(APK, IP)
            installAPK(TEST_APK, IP)
            
            #run unit test
            #test package/runner
            runTests(TEST_PACKAGE, TEST_RUNNER, DEVICE, IP)
            
            #remove apk
            removeAPK(PACKAGE, IP)
            
            stopDevice(IP)
            
        except subprocess.CalledProcessError as e:
            print "Unable to test on device " + DEVICE
        
    #stop emulators
    #stopDevice()
    time.sleep(DELAY)
    
    print "Finished testing all devices!"
        
def findAPK(package, IP):
    #SCRIPT = 'adb '
    PARAMS = ' shell pm path ' + package
    
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
    if OUTPUT != "":
        return True
    
    return False
    
def installAPK(apkName, IP):
    #install apk on emulator
    #SCRIPT = 'adb '
    PARAMS = ' install "' + apkName + '"'
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
    print OUTPUT
    
def removeAPK(package, IP):
    #remove apk on emulator
    #SCRIPT = 'adb '
    PARAMS = ' uninstall "' + package + '"'
    
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
def runTests(PACKAGE, RUNNER, DEVICE, IP):
    #start the tests
    #SCRIPT = 'adb '
    PARAMS = ' shell am instrument -w ' + PACKAGE + '/' + RUNNER
    CMD = ADB_SCRIPT + IP + PARAMS
        
    OUTPUT = subprocess.check_output(CMD)
    
    writeLog(OUTPUT, DEVICE)
    
def startDevice(deviceName):
    print "Starting device: " + deviceName
    #start emulator
    SCRIPT = '"' + PATH + 'player" '
    PARAMS = '--vm-name "' + deviceName + '"'
    CMD = SCRIPT + PARAMS
    
    subprocess.Popen(CMD, shell=True)
    
def stopDevice(IP):
    #stop emulator
    #CMD = 'taskkill /IM player.exe'
    #PARAMS = ' '
    #CMD = ADB_SCRIPT + IP + PARAMS
    #command to use: tasklist /v /fi "imagename eq player.exe"
    subprocess.check_output(CMD)
    
    
def getGenyshellDevices():
    #return device list
    GENY_BATCH = PATH + 'genyshell'
    GENY_PARAMS = '-c "devices show"'
    
    CMD = GENY_BATCH + " " + GENY_PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
    return OUTPUT
    
def getMapOfIPs():
    #key is of IP, value is of name
    DELIM = "virtual"
    
    STR_LIST = {}
    STR_LIST = getGenyshellDevices().split(DELIM)[4:]
    
    DELIM = "|"
    DEVICE_MAP = {}
    #create map
    for line in STR_LIST:
        SPLIT = line.split(DELIM)
        IP = SPLIT[1].strip() + ":5555"
        if "0.0.0.0" not in IP:
            DEVICE_NAME = SPLIT[2].strip()
            DEVICE_MAP[IP] = DEVICE_NAME
    
    return DEVICE_MAP
    
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
    
def writeLog(OUTPUT, DEVICE):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    FILENAME = time.strftime("%Y-%m-%d") + "." + DEVICE.replace(" ","")
    FILE = open(LOG_DIR + "/" + FILENAME, 'w')
    FILE.write(OUTPUT)
    FILE.close()
    
main(sys.argv)