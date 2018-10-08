import ROOT
import sys,os
import pickle
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Compute xsec per module from pcc ntuples and given xsec')
parser.add_argument('-d','--dir',  type=str, default="", help='Directory of AlCaPCC to input')
parser.add_argument('-f','--file', type=str, default="", help='The AlCaPCC file to input')
parser.add_argument('-fl','--flist',type=argparse.FileType('r'), help='File list of AlCaPCC to input')
parser.add_argument('--xsec', type=float, default=9e6, help='Total pcc xsec')
parser.add_argument('-l','--label',type=str, default="test", help='Label for output file')
parser.add_argument('-r','--run',default=0, help='Run to select')

args=parser.parse_args()

filelist=[]
if args.file=="" and args.dir=="" and args.flist=="":
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

if args.flist!="":
    try: 
        with args.flist as f: 
            print "opening list ",f
            lines = f.readlines()
            for line in lines:
                filelist.append(line.split('\n')[0])
    except:
        print "File Read Error!"
#print "the file list ",filelist

PCCinMod={}
PCCinMod["total"]=0
iFile=0
numBunch=3564
txtfile=open("modlist_"+args.label+".txt","wb")

for filename in filelist:
    print filename
    tfile=ROOT.TFile.Open(filename)
    try:
        tree=tfile.Get("LuminosityBlocks")
        nEntries=tree.GetEntries()
    except:
        print "error in TTree... probably empty"
        continue 
    
    print "nEntries",nEntries
    
    for iEnt in range(nEntries):
        tree.GetEntry(iEnt)
        if iEnt%50==1:
            print "Working on Lumiblock ",iEnt
        
        #if args.run!=0:
        #    if str(tree.run)!=str(args.run):
        #        continue
        
        counts=tree.recoPixelClusterCounts_alcaPCCProducerZeroBias_alcaPCCZeroBias_RECO.readCounts()
        modIDs=tree.recoPixelClusterCounts_alcaPCCProducerZeroBias_alcaPCCZeroBias_RECO.readModID()
        #events=tree.recoPixelClusterCounts_alcaPCCProducerZeroBias_alcaPCCZeroBias_RECO.readEvents()
        #print "len",len(counts),len(modIDs),len(events)
        #for i in range(len(counts)):
        #    print counts[i]
        #print "bunch crossing ID? , ",counts[0],counts[3564],counts[7128]
        #print len(modIDs),len(counts)
        
        for i in range(len(counts)):
            #print i,modIDs[i]
            #bxid=
            if (i%numBunch==0):
                try: 
                    module=modIDs[i/numBunch]
                except:
                    print "data error"
                    module=0
        #Still need to add layer 1 veto or something?!
        #clusters=item[1]
        ##if layer!=1:
            if not PCCinMod.has_key(module):
                PCCinMod[module]=0.0
            if (counts[i]==0): 
                continue 
            PCCinMod[module]=PCCinMod[module]+counts[i]
            PCCinMod["total"]=PCCinMod["total"]+counts[i]
            
    tfile.Close() 
    iFile=iFile+1

print "PCCMod, total",PCCinMod["total"]

xsecPerMod={}
for mod in PCCinMod:
    if mod=="total":
        continue
    xsecPerMod[mod]=PCCinMod[mod]/PCCinMod["total"] * args.xsec
    print mod, xsecPerMod[mod]
    txtfile.write(str(mod))
    txtfile.write("\n")

rawfile=open("rawcounts_"+args.label+".pkl","wb")
pickle.dump(PCCinMod,rawfile)
rawfile.close()

outfile=open("output_"+args.label+".pkl","wb")
pickle.dump(xsecPerMod,outfile)
outfile.close()
    
    
