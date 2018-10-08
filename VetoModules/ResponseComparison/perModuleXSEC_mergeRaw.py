import ROOT
import sys,os
import pickle
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Compute xsec per module from raw pcc in pickle files and given xsec')
parser.add_argument('-d','--dir',  type=str, default="", help='Director of pcc ntuples to input')
parser.add_argument('--xsec', type=float, default=1, help='Total pcc xsec')
parser.add_argument('-l','--label',type=str, default="test", help='Label for output file')
parser.add_argument('--veto',default="", help='Vetolist')
parser.add_argument('--layer',type=int,default=0, help='omit layer')

args=parser.parse_args()

filelist=[]
if args.dir=="":
    print "No file to process"
    sys.exit(-1)

vetoList=[]
if args.veto!="":
    try:
        vetoListFile=open(args.veto)
        for line in vetoListFile.readlines():
            try:
                vetoList.append(int(line))
            except:
                print "failed", line
        vetoListFile.close()
    except:
        print "Can't open",args.veto

for filename in os.listdir(args.dir):
    if filename.find(".pkl")!=-1:
        if filename.find("raw")!=-1:
            filelist.append(args.dir+"/"+filename)

print "n Mods to veto",len(vetoList)

PCCinMod={}
PCCinMod["total"]=0
iFile=0
for filename in filelist:
    print filename
    try:
        rawFile=open(filename)
        PCCinModFromFile=pickle.load(rawFile)
        rawFile.close()
    except:
        print "Error in reading pkl file,",filename
        continue
    for module in PCCinModFromFile.keys():
        if module=="total":
            continue
        if module in vetoList:
            continue
        if args.layer==1:
            if int(module) <= 304000000:
                continue 
        if not PCCinMod.has_key(module):
            PCCinMod[module]=0.0
        PCCinMod[module]=PCCinMod[module]+PCCinModFromFile[module]
        PCCinMod["total"]=PCCinMod["total"]+PCCinModFromFile[module]

print PCCinMod["total"]

xsecPerMod={}
xsecSum=0
for mod in PCCinMod:
    if mod=="total":
        continue
    if mod in vetoList:
        continue
    xsecPerMod[mod]=PCCinMod[mod]/PCCinMod["total"] * args.xsec
    print mod, xsecPerMod[mod]
    xsecSum=xsecSum+xsecPerMod[mod]

print "sum",xsecSum

rawfile=open("rawcounts_"+args.label+".pkl","wb")
pickle.dump(PCCinMod,rawfile)
rawfile.close()

outfile=open("output_"+args.label+".pkl","wb")
pickle.dump(xsecPerMod,outfile)
outfile.close()
    
    

