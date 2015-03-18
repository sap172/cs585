#this script runs the app tests against all the running devices

#importing libraries
import os, sys, subprocess, time, getopt
from multiprocessing import Process, freeze_support

PATH = 'C:\\Program Files\\Genymobile\\Genymotion\\'
APK = 'app-debug.apk'
TEST_APK = 'app-debug-test-unaligned.apk'
PACKAGE = 'com.twooilyplumbers.simplecalculator'
TEST_PACKAGE = 'com.twooilyplumbers.simplecalculator.test'
TEST_RUNNER = 'android.test.InstrumentationTestRunner'
LOG_DIR = 'logs'
ADB_SCRIPT = 'adb -s '
VERBOSE = False

def main():
    
    print APK
    
    IP_MAP = getMapOfIPs()
          
    for IP, DEVICE in IP_MAP.iteritems():
        process = Process(target=splitProcesses, args=(IP,DEVICE))
        process.start()
        process.join()
            
    print "Finished testing all devices!"
        
def splitProcesses(IP, DEVICE):
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
        
    except subprocess.CalledProcessError as e:
        print "Unable to test on device " + DEVICE
            
def findAPK(package, IP):
    #find the apk on the device
    PARAMS = ' shell pm path ' + package
    
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
    if OUTPUT != "":
        return True
    
    return False
    
def installAPK(apkName, IP):
    #install apk on emulator
    PARAMS = ' install "' + apkName + '"'
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
    print OUTPUT
    
def removeAPK(package, IP):
    #remove apk on emulator
    PARAMS = ' uninstall "' + package + '"'
    
    CMD = ADB_SCRIPT + IP + PARAMS
    
    OUTPUT = subprocess.check_output(CMD)
    
def runTests(PACKAGE, RUNNER, DEVICE, IP):
    #start the tests
    PARAMS = ' shell am instrument -w ' + PACKAGE + '/' + RUNNER
    CMD = ADB_SCRIPT + IP + PARAMS
        
    OUTPUT = subprocess.check_output(CMD)
    
    writeLog(OUTPUT, DEVICE)
    
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
    STR_LIST = getGenyshellDevices().split(DELIM)[3:]
    
    DELIM = "|"
    DEVICE_MAP = {}
    #create map
    for line in STR_LIST:
        SPLIT = line.split(DELIM)
        IP = SPLIT[1].strip() + ":5555"
        if "0.0.0.0" not in IP:
            DEVICE_NAME = SPLIT[2].strip()
            DEVICE_MAP[IP] = DEVICE_NAME[:-5]
    
    return DEVICE_MAP
    
def writeLog(OUTPUT, DEVICE):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    FILENAME = time.strftime("%Y-%m-%d") + "." + DEVICE.replace(" ","")
    FILE = open(LOG_DIR + "/" + FILENAME, 'w')
    FILE.write(OUTPUT)
    FILE.close()
    
    #prints on shell if verbose is true
    if VERBOSE = True:
        print OUTPUT
   
def getHelpString():
    #returns help string
    USAGE = ("tester.py <-h><-v>" +
             "<--APK> file" +
             "<--testAPK> file" +
             "<--delay> seconds" +
             "<--runner> runner" +
             "<--log> log file" +
             "<--path> path" +
             "<--package> package")
    return USAGE
   
def parseOptions(argv):
    #parses the input arguments
    try:
        options, args = getopt.getopt(argv,"hv:",["APK=", "testAPK=", 
        "delay=", "runner=", "log=", "path=", "package="])

    except getopt.GetoptError as e:
        print str(err)
        print getHelpString()
        sys.exit(2)
        
    #parse options
    '''if not options:
        #empty input
        print getHelpString
        sys.exit()
    '''
    
    for opt, arg in options:
        if opt == "-h":
            #print help string
            print getHelpString()
        if opt == "-v":
            #set verbose
            VERBOSE = True
        if opt == "--delay":
            #set delay
            DELAY = arg
        if opt == "--runner":
            #set runner
            RUNNER = arg
        if opt == "--log":
            #set log
            LOG_DIR = arg
        if opt == "--path":
            #set path
            PATH = arg
        if opt == "--package":
            #set package
            PACKAGE = arg
        if opt == "--APK":
            #set apk
            APK = arg
        if opt == "--testAPK":
            #set test apk
            TEST_APK = arg
        
    
if __name__ == '__main__':
    parseOptions(sys.argv[1:])
    freeze_support() 
    main()