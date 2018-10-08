import pickle
import sys,os
import ROOT
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--files", help="Comma-separated list of file paths.")
parser.add_argument("--vetoList", default="", help="Veto list file name.")
parser.add_argument("--labels", default="", help="Comma-separated list of labels for two files")
parser.add_argument("--outdir", default=".", help="Output directory")
parser.add_argument("-b","--batch", default=0, help="In batch mode?")
parser.add_argument("-g","--gauses", type=int, default=1, help="How many gaussians to fit?")
parser.add_argument("-w","--width", type=float, default=0.05, help="Width of ratio PLOTS")
args=parser.parse_args()

if args.batch!=0:
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

filename1=args.files.split(",")[0]
filename2=args.files.split(",")[1]
vetoList=[]
if args.vetoList!="":
    vetoListFile=open(args.vetoList)
    for line in vetoListFile.readlines():
        try:
            vetoList.append(int(line))
        except:
            print "failed", line
    vetoListFile.close()
if args.labels=="":
    label1=filename1.split(".")[0]
    label2=filename2.split(".")[0]
else:
    label1=args.labels.split(",")[0]
    label2=args.labels.split(",")[1]

file1=open(filename1)
file2=open(filename2)

dict1=pickle.load(file1)
dict2=pickle.load(file2)

mods1=dict1.keys()
mods2=dict2.keys()

commonMods=list(set(mods1).intersection(mods2))
dMods1=set(mods1)-set(mods2)
dMods2=set(mods2)-set(mods1)
differentMods=list(dMods1.union(dMods2))

print len(mods1),len(mods2),len(commonMods),len(differentMods)

#ratio=ROOT.TH1F("ratio","",100,0.75,1.25)
#ratioFilter=ROOT.TH1F("ratioFilter","",100,0.75,1.25)
ratio=ROOT.TH1F("ratio","",100,1-args.width,1+args.width)
#ratioFilter=ROOT.TH1F("ratioFilter","",100,1-args.width,1+args.width)
rel1=ROOT.TH1F("rel1",";Relative Response;Number of Modules",40,0.0,0.004)
rel2=ROOT.TH1F("rel2","",40,0.0,0.004)

iCount=0
xsec1=0
xsec2=0
xsecRegion1={}
xsecRegion2={}

low=[]
lowp=0
lowm=0
high=[]
highp=0
highm=0

modList={}
modFile=open("../modList.txt")
#modFile=open("2018MasterModlist.txt")
for line in modFile.readlines():
    items=line.split()
    if len(items)==0:
        continue
    #items=line.split('\n')
    mod=int(items[0])
    #fullName=items[1]
    #if fullName.split("_")[1].find("p")!=-1:
    #    plusOrMinus=1
    #elif fullName.split("_")[1].find("m")!=-1:
    #    plusOrMinus=-1
    #else:
    #    print "No m or p",mod,fullName.split("_")[1]
    #modList[mod]=plusOrMinus
    #modList[mod]=fullName
    if not mod in modList:
        modList[mod]=1
    else:
        modList[mod]+=1
modFile.close()

counters={}
counters["FPix"]={}
counters["BPix"]={}
for iPix in counters:
    counters[iPix][1]={}
    counters[iPix][-1]={}
    for i in counters[iPix]:
        counters[iPix][i]["up"]=0
        counters[iPix][i]["down"]=0
lostMods=[]
newVeto=[]
n2Veto=[]

outfile=open(args.outdir+"lostlist_"+args.labels.split(",")[1]+".txt","wb")
vetofile=open(args.outdir+"veto_"+args.labels.split(",")[1]+".txt","wb")
VdMLocResFileL=open("VdMLocResFileLow","w")
VdMLocResFileH=open("VdMLocResFileHigh","w")

for mod in commonMods:
    if mod in vetoList:
        print "skipping",mod
        continue
    #if dict1[mod]/dict2[mod]<0.97 or dict1[mod]/dict2[mod]>1.01:
    #if abs(1-dict1[mod]/dict2[mod])>.1:
    #    print mod,dict1[mod],dict2[mod],dict1[mod]/dict2[mod]
    else:
        ratio.Fill(dict1[mod]/dict2[mod])
        if dict1[mod]/dict2[mod] >1.0:
           VdMLocResFileH.write(str(mod)) 
           VdMLocResFileH.write("\n") 
        if dict1[mod]/dict2[mod] <1.0:
           VdMLocResFileL.write(str(mod)) 
           VdMLocResFileL.write("\n") 
           
###Change this to set the veto list window, not the display window
        #if (dict1[mod]/dict2[mod] > 1.7 or dict1[mod]/dict2[mod] < 1.45):#AV
        #if (dict1[mod]/dict2[mod] > 1.05 or dict1[mod]/dict2[mod] < 0.95):#AV2
        #if (dict1[mod]/dict2[mod] > 1.65 or dict1[mod]/dict2[mod] < 1.35):#BV
        #if (dict1[mod]/dict2[mod] > 1.05 or dict1[mod]/dict2[mod] < 0.95):#BV2
        #if (dict1[mod]/dict2[mod] > 1.65 or dict1[mod]/dict2[mod] < 1.37):#CV
        #if (dict1[mod]/dict2[mod] > 1.05 or dict1[mod]/dict2[mod] < 0.95):#CV2
        #if (dict1[mod]/dict2[mod] > 1.65 or dict1[mod]/dict2[mod] < 1.4):#DV
        #if (dict1[mod]/dict2[mod] > 1.05 or dict1[mod]/dict2[mod] < 0.95):#DV2
        #if (dict1[mod]/dict2[mod] > 1.05 or dict1[mod]/dict2[mod] < 1.03):#BA
        #if (dict1[mod]/dict2[mod] > 1.0525 or dict1[mod]/dict2[mod] < 1.015):#CA
        #if (dict1[mod]/dict2[mod] > 1.045 or dict1[mod]/dict2[mod] < 1.005):#DA
        #if (dict1[mod]/dict2[mod] > 1.005 or dict1[mod]/dict2[mod] < 0.985):#CB
        if (dict1[mod]/dict2[mod] > 1.005 or dict1[mod]/dict2[mod] < 0.965):#DB
        #if (dict1[mod]/dict2[mod] > 1.01 or dict1[mod]/dict2[mod] < 0.99):#DC
            n2Veto.append(mod)
        iCount=iCount+1
        xsec1=xsec1+dict1[mod]
        xsec2=xsec2+dict2[mod]
        #if not modList.has_key(mod):
            #print "Module not in master list?... ",mod
        #    lostMods.append(mod)
        #    continue  
        ##location=modList[mod].split("_")[0]
        ##locationPlusMinus=location+"_"+modList[mod].split("_")[1]#+"_"+modList[mod].split("_")[2]
        ##if modList[mod].split("_")[1].find("p")!=-1:
        ##    plusOrMinus=1
        ##elif modList[mod].split("_")[1].find("m")!=-1:
        ##    plusOrMinus=-1
        ##else:
        ##    print "No m or p",mod,modList[mod].split("_")[1]
        ##upDown=""
        ##if dict1[mod]/dict2[mod]<1:
        ##    low.append(mod)
        ##    upDown="down"
        ##else:    
        ##    high.append(mod)
        ##    upDown="up"
        ##counters[location][plusOrMinus][upDown]=counters[location][plusOrMinus][upDown]+1
        ##
        ##if locationPlusMinus not in xsecRegion1:
        ##    xsecRegion1[locationPlusMinus]=0
        ##xsecRegion1[locationPlusMinus]=xsecRegion1[locationPlusMinus]+dict1[mod]
        ##
        ##if locationPlusMinus not in xsecRegion2:
        ##    xsecRegion2[locationPlusMinus]=0
        ##xsecRegion2[locationPlusMinus]=xsecRegion2[locationPlusMinus]+dict2[mod]

    if abs(1-dict1[mod]/dict2[mod])>.13 or dict1[mod]<1000 or dict2[mod]<1000:
        print mod,dict1[mod],dict2[mod],dict1[mod]/dict2[mod]
        if mod not in newVeto:
            newVeto.append(mod)

VdMLocResFileL.close()
VdMLocResFileH.close()
print "New Veto based on cut, "
for mod in n2Veto:
        print mod
        vetofile.write(str(mod))
        vetofile.write("\n") 
#vetofile.close()

print "different mods"
for mod in differentMods:
        print mod
        vetofile.write(str(mod))
        vetofile.write("\n")
vetofile.close()
outfile.close()

#locations=xsecRegion1.keys()
#locations.sort()
print "Ratios",args.labels

dict={}
if os.path.isfile("ratioFile2.pkl"):
    ratioFile=open("ratioFile2.pkl")
    dict=pickle.load(ratioFile)
    ratioFile.close()

dict[args.labels.split(",")[1]]={}
#for locationPlusMinus in locations:
#    print locationPlusMinus,"1,2,2/1,",xsecRegion1[locationPlusMinus],xsecRegion2[locationPlusMinus],xsecRegion2[locationPlusMinus]/xsecRegion1[locationPlusMinus]
#    dict[args.labels.split(",")[1]][locationPlusMinus]=xsecRegion2[locationPlusMinus]/xsecRegion1[locationPlusMinus]

ratioFile=open(args.outdir+"ratioFile2.pkl","w")
pickle.dump(dict,ratioFile)
ratioFile.close()

newVeto.sort()
print "newVeto"+label2+"=",newVeto

#for iPix in counters:
#    for plus in counters[iPix]:
#        for up in counters[iPix][plus]:
#            print iPix,plus,up,counters[iPix][plus][up]


#print "low,high",len(low),len(high)
#print "lowp,lowm,highp,highm",lowp,lowm,highp,highm
#raw_input()
for mod in commonMods:
    if mod in vetoList:
        continue
    else:
        rel1.Fill(dict1[mod]/xsec1)
        rel2.Fill(dict2[mod]/xsec2)

    #if mod not in newVeto:
    #    ratioFilter.Fill(dict1[mod]/dict2[mod])


print "iCount",iCount
print "xsecs", xsec1,xsec2
    
file1.close()
file2.close()

can=ROOT.TCanvas("can","",1000,700)
nbins=ratio.GetNbinsX()
binN=ratio.GetBinContent(nbins)
binNplus1=ratio.GetBinContent(nbins+1)
ratio.SetBinContent(nbins,binN+binNplus1)
bin0=ratio.GetBinContent(0)
bin1=ratio.GetBinContent(1)
ratio.SetBinContent(1,bin0+bin1)
ratio.Draw()
ratio.SetTitle(";"+label1+"/"+label2+";Modules")
twoGaus=ROOT.TF1("twoGaus","gaus(0)+gaus(3)",0.9,1.1)
twoGaus.SetParameter(0,100)
twoGaus.SetParameter(1,0.985)
twoGaus.SetParameter(2,0.003)
twoGaus.SetParameter(3,100)
twoGaus.SetParameter(4,1.010)
twoGaus.SetParameter(5,0.003)
if args.gauses==2:
    ratio.Fit(twoGaus)
elif args.gauses==1:
    ratio.Fit("gaus")
#print "Histo mean",label2,ratioFilter.GetMean(),ratio.GetRMS(),ratio.GetMeanError()

can.Update()
can.SaveAs(args.outdir+"ratio_"+label1+"over"+label2+".png")

#nbins=ratioFilter.GetNbinsX()
#binN=ratioFilter.GetBinContent(nbins)
#binNplus1=ratioFilter.GetBinContent(nbins+1)
#ratioFilter.SetBinContent(nbins,binN+binNplus1)
#bin0=ratioFilter.GetBinContent(0)
#bin1=ratioFilter.GetBinContent(1)
#ratioFilter.SetBinContent(1,bin0+bin1)
#ratioFilter.Draw()
#ratioFilter.SetTitle(";"+label1+"/"+label2+";Modules")
#twoGaus=ROOT.TF1("twoGaus","gaus(0)+gaus(3)",0.9,1.1)
#twoGaus.SetParameter(0,100)
#twoGaus.SetParameter(1,0.985)
#twoGaus.SetParameter(2,0.003)
#twoGaus.SetParameter(3,100)
#twoGaus.SetParameter(4,1.010)
#twoGaus.SetParameter(5,0.003)
#if args.gauses==2:
#    ratioFilter.Fit(twoGaus)
#elif args.gauses==1:
#    ratioFilter.Fit("gaus")
#print "Histo mean",args.labels[1],ratioFilter.GetMean(),ratio.GetRMS()

can.Update()
#can.SaveAs(args.outdir+"ratio_"+label1+"over"+label2+"_Filter.png")

leg=ROOT.TLegend(0.7,0.9,0.7,0.9)
rel1.Draw("hist")
rel2.SetLineColor(633)
rel2.Draw("histsame")
leg.AddEntry(rel1,label1,"l")
leg.AddEntry(rel2,label2,"l")
leg.Draw("same")

can.Update()
can.SaveAs(args.outdir+"relativeResponse_"+label1+"_"+label2+".png")
