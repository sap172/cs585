import os, sys, subprocess, time

PATH = 'C:\\Program Files\\Genymobile\\Genymotion\\'
#APK = 'C:\\Users\\parkin\\AndroidstudioProjects\\SimpleCalculator\\app\\build\\outputs\\apk\\app-debug.apk'
APK = 'app-debug.apk'
#TEST_APK = 'C:\\Users\\parkin\\AndroidstudioProjects\\SimpleCalculator\\app\\build\\outputs\\apk\\app-debug-test-unaligned.apk'
TEST_APK = 'app-debug-test-unaligned.apk'
PACKAGE = 'com.twooilyplumbers.simplecalculator'
TEST_PACKAGE = 'com.twooilyplumbers.simplecalculator.test'
TEST_RUNNER = 'android.test.InstrumentationTestRunner'
LOG_DIR = 'logs'
DELAY = 60

def main(args):
    
    print APK
    
    #array of emulators
    DEVICE_LIST = createDeviceList()
    
    for DEVICE in DEVICE_LIST:
        try:
            #start emulators
            startDevice(DEVICE)
            time.sleep(DELAY)
            APK_EXISTS = findAPK(PACKAGE)
            if APK_EXISTS:
                removeAPK(PACKAGE)
                
            APK_EXISTS = findAPK(PACKAGE + '.test')
            if APK_EXISTS:
                removeAPK(PACKAGE + '.test')
            
            print "Installing APK..."
            installAPK(APK)
            installAPK(TEST_APK)
            
            #run unit test
            #test package/runner
            runTests(TEST_PACKAGE, TEST_RUNNER, DEVICE)
            
            #remove apk
            removeAPK(PACKAGE)
            
        except subprocess.CalledProcessError as e:
            print "Unable to test on device " + DEVICE
        
        #stop emulator
        stopDevice()
        time.sleep(DELAY)
        
    print "Finished testing all devices!"
        
def findAPK(package):
    SCRIPT = 'adb '
    PARAM = '-e shell pm path ' + package
    
    CMD = SCRIPT + PARAM
    
    OUTPUT = subprocess.check_output(CMD)
    
    if OUTPUT != "":
        return True
    
    return False
    
def installAPK(apkName):
    #install apk on emulator
    SCRIPT = 'adb '
    PARAM = '-e install "' + apkName + '"'
    CMD = SCRIPT + PARAM
    
    OUTPUT = subprocess.check_output(CMD)
    
    print OUTPUT
    
def removeAPK(package):
    #remove apk on emulator
    SCRIPT = 'adb '
    PARAM = '-e uninstall "' + package + '"'
    
    CMD = SCRIPT + PARAM
    
    OUTPUT = subprocess.check_output(CMD)
    
def runTests(PACKAGE, RUNNER, DEVICE):
    #start the tests
    SCRIPT = 'adb '
    PARAM = 'shell am instrument -w ' + PACKAGE + '/' + RUNNER
    CMD = SCRIPT + PARAM
        
    OUTPUT = subprocess.check_output(CMD)
    
    writeLog(OUTPUT, DEVICE)
    
def startDevice(deviceName):
    print "Starting device: " + deviceName
    #start emulator
    SCRIPT = '"' + PATH + 'player" '
    PARAM = '--vm-name "' + deviceName + '"'
    CMD = SCRIPT + PARAM
    
    subprocess.Popen(CMD, shell=True)
    
def stopDevice():
    #stop emulator
    CMD = 'taskkill /IM player.exe'
    
    subprocess.check_output(CMD)
    
def createDeviceList():
    #parse phone list
    GENY_BATCH = PATH + 'genyshell'
    GENY_PARAMS = '-c "devices show"'
    DELIM = "0.0.0.0"
    
    CMD = GENY_BATCH + " " + GENY_PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    STR_LIST = {}
    STR_LIST = OUTPUT.split(DELIM)[1:]
  
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