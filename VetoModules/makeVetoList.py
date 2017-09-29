import sys, os
import argparse

parser = argparse.ArgumentParser(description='Find a ROOT file among many with the run number you input.')
parser.add_argument('-r', '--runs', type=str, default="", help="Comma-separated list of runs to find vetoed modules in (e.g. 262204,262205,262235)")
parser.add_argument('--modStrToNum',  default="modList.txt", help="Text file containing lines like \'302055700 BPix_BpI_SEC4_LYR1_LDR5F_MOD1\'")
parser.add_argument('-o', '--output', default="vetoModules.txt", help="Name of output file.")
#parser.add_argument('--pathFlag', default="pixel", help="pixel for established list; pixelscratch/pixelscratch for new lists")
parser.add_argument('-j', '--json', default="", help="Input a CMS json file to generate a list of runs to check")
args = parser.parse_args()

if args.runs=="" and args.json=="":
    print "No runs to search.  Exiting."
    sys.exit(1)

##1) Identify a run number associated with the fill. 
##For example for fill 4634 run 262081. 
##You can take them from WBM for the fill you are interested in.
##https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/FillReport
if args.runs!="":
    runs=args.runs.split(",")
elif args.json!=0:
    import json
    jsonfile=open(args.json)
    jsondict=json.load(jsonfile)
    runs=jsondict.keys()
    runs.sort()
    for iRuns in range(len(runs)):
        runs[iRuns]=str(runs[iRuns])

globalConfigKeys=[]

moduleStrToNum={}
modLines=[]
if os.path.isfile(args.modStrToNum):
    modStrToNumFile=open(args.modStrToNum)
    modLines=modStrToNumFile.readlines()
    modStrToNumFile.close()
else:
    print "No ",args.modStrToNum

for modLine in modLines:
    try:
        num=int(modLine.split()[0])
        string=modLine.split()[1]
        moduleStrToNum[string]=num
    except:
        print "Can't do",modLine


##2) Login to srv-c2f38-16-01. (Requires cmsusr account/login first.) 
##Look into the file 
##/pixel/data0/Run_262000/Run_262081/PixelConfigurationKey.txt 
##and note the configuration key number, in this case: 
##100965
for run in runs:
    runDir=int(run)/1000
    runDir=runDir*1000
    #pixelConfigFileName="/"+args.pathFlag+"/data0/Run_"+str(runDir)+"/Run_"+str(run)+"/PixelConfigurationKey.txt"
    pixelConfigFileName="/pixel/data0/Run_"+str(runDir)+"/Run_"+str(run)+"/PixelConfigurationKey.txt"
    if os.path.isfile(pixelConfigFileName):
        pixelConfigFile=open(pixelConfigFileName)
    else:
        print "No ",pixelConfigFileName,
        print "Try pixelscratch/pixelscratch"
        pixelConfigFileName="/pixelscratch/pixelscratch/data0/Run_"+str(runDir)+"/Run_"+str(run)+"/PixelConfigurationKey.txt"
        if os.path.isfile(pixelConfigFileName):
            pixelConfigFile=open(pixelConfigFileName)
            print "OK!"
        else:
            print "No ",pixelConfigFileName
            continue

    lines=pixelConfigFile.readlines()
    for line in lines:
        if line.find("Pixel Global Configuration Key = ")!=-1:
            key=(line.split("Pixel Global Configuration Key = ")[1]).split("\n")[0]
            #print key
            if key not in globalConfigKeys:
                globalConfigKeys.append(key)

    pixelConfigFile.close()
    
print "globalConfigKeys",globalConfigKeys


##3) Search the file 
##/pixelscratch/pixelscratch/config/Pix/configurations.txt 
##for the string "key 100965" and note the detconfig version which is just below. 
## 
##In this case: 
##
##key 100965 
##detconfig   95 
##
##This identifies the version of the detconfig file = 95.  


pixelCfgMapFileName="/pixelscratch/pixelscratch/config/Pix/configurations.txt"
if  os.path.isfile(pixelCfgMapFileName):
    pixelCfgMapFile=open(pixelCfgMapFileName)
else:
    print "No",pixelCfgMapFileName
    sys.exit(1)

pixelCfgMapLines=pixelCfgMapFile.readlines()
pixelCfgMapFile.close()

detConfigs=[]

iLine=0
for iLine in range(len(pixelCfgMapLines)):
    print iLine,pixelCfgMapLines[iLine]
    mapLine=pixelCfgMapLines[iLine]
    if mapLine.find("key ")!=-1:
        key=mapLine.split()[1]
        if key in globalConfigKeys:
            iLoop=1
            while iLoop<40:
                if pixelCfgMapLines[iLine+iLoop].find("detconfig")!=-1:
                    thisdetconfig=pixelCfgMapLines[iLine+iLoop].split()[1]
                    #print thisdetconfig
                    if thisdetconfig not in detConfigs:
                        detConfigs.append(thisdetconfig)
                    break
                #if you find the next one, stop
                if pixelCfgMapLines[iLine+iLoop].find("key")!=-1:
                    print "Didn't find detconfig"
                    break
                iLoop=iLoop+1
                

print "detector configurations",detConfigs

badModules=[]

##4) You can see the disabled modules in the file 
##/pixelscratch/pixelscratch/config/Pix/detconfig/95/detectconfig.dat 
## 
##Now you can search for the module with the "noAnalogSignal" string. 
for detConfig in detConfigs:
    detectorConfigFileName="/pixelscratch/pixelscratch/config/Pix/detconfig/"+detConfig+"/detectconfig.dat"
    detectorConfigFile=open(detectorConfigFileName)

    lines=detectorConfigFile.readlines()
    detectorConfigFile.close()

    for line in lines:
        if line.find("noAnalogSignal")!=-1:
            ## if any ROC is missing remove the entire module
            module=line.split("_ROC")[0]
            if module not in badModules:
                badModules.append(module)

badModules.sort()
print "(n) bad modules (",len(badModules),") ",badModules

##write out the module numbers to a file
outputFile=open(args.output,"w")
print "Writing bad module numbers to",args.output
for badModule in badModules:
    if moduleStrToNum.has_key(badModule):
        outputFile.write(str(moduleStrToNum[badModule])+"\n")
    else:
        print "modulesStrToNum has no key for",badModule
outputFile.close()
                


