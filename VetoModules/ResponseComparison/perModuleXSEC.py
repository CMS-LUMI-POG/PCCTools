import ROOT
import sys,os
import pickle
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Compute xsec per module from pcc ntuples and given xsec')
parser.add_argument('-d','--dir',  type=str, default="", help='Director of pcc ntuples to input')
parser.add_argument('-f','--file', type=str, default="", help='The pcc ntuple to input')
parser.add_argument('--xsec', type=float, default=9e6, help='Total pcc xsec')
parser.add_argument('-l','--label',type=str, default="test", help='Label for output file')
parser.add_argument('-r','--run',default=0, help='Run to select')

args=parser.parse_args()

filelist=[]
if args.file=="" and args.dir=="":
    print "No file to process"
    sys.exit(-1)

if args.file!="":
    filelist.append(args.file)

if args.dir!="":
    if args.dir.find("/store")==0:
        filenames=subprocess.check_output(["/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select","ls", args.dir])
        filenames=filenames.split("\n")
        for filename in filenames:
            if filename.find(".root")!=-1:
                filelist.append("root://eoscms//eos/cms"+args.dir+filename)
    else:
        for filename in os.listdir(args.dir):
            filelist.append(args.dir+"/"+filename)

    
PCCinMod={}
PCCinMod["total"]=0
iFile=0
for filename in filelist:
    print filename
    tfile=ROOT.TFile.Open(filename)
    tree=tfile.Get("lumi/tree")
    tree.SetBranchStatus("*",0)
    tree.SetBranchStatus("*nPixelClusters*",1)
    tree.SetBranchStatus("*layers*",1)
    if args.run!=0:
        tree.SetBranchStatus("*run*",1)

    nEntries=tree.GetEntries()
    
    print "nEntries",nEntries
    
    for iEnt in range(nEntries):
        tree.GetEntry(iEnt)
        if iEnt%10000==1:
            print iEnt
        
        if args.run!=0:
            if str(tree.run)!=str(args.run):
                continue
        
        print "len(tree.nPixelClusters)",len(tree.nPixelClusters)
        for item in tree.nPixelClusters:
            bxid=item[0][0]
            module=item[0][1]
            layer=tree.layers[module]
            clusters=item[1]
            if layer!=1:
                if not PCCinMod.has_key(module):
                    PCCinMod[module]=0.0
                PCCinMod[module]=PCCinMod[module]+clusters
                PCCinMod["total"]=PCCinMod["total"]+clusters
    tfile.Close() 
    iFile=iFile+1

print PCCinMod["total"]

xsecPerMod={}
for mod in PCCinMod:
    if mod=="total":
        continue
    xsecPerMod[mod]=PCCinMod[mod]/PCCinMod["total"] * args.xsec
    print mod, xsecPerMod[mod]

rawfile=open("rawcounts_"+args.label+".pkl","wb")
pickle.dump(PCCinMod,rawfile)
rawfile.close()

outfile=open("output_"+args.label+".pkl","wb")
pickle.dump(xsecPerMod,outfile)
outfile.close()
    
    
