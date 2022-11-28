import ROOT 
import numpy as np 
import sys, os
from math import exp
import argparse
import subprocess
import array

parser=argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", default="", help="inputLumiInfo")
parser.add_argument("-a", "--all", default=True, help="Apply both the type1 and type2 correction")
parser.add_argument("--quadTrainCorr", default=0.00, help="Apply a quadratic correction to in-train BXs (Default:  0.02 ub/Hz)")
parser.add_argument("--noType1", action='store_true', default=False, help="Only apply the type2 correction")
parser.add_argument("--noType2", action='store_true', default=False, help="Only apply the type1 correction")
parser.add_argument('-b', '--batch',   action='store_true', default=False, help="Batch mode (doesn't make GUI TCanvases)")
parser.add_argument('-p', '--par', default="0.074,0.0,0.00086,0.014", help="The parameters for type1 and type2 correction (0.074,0.0,0.00086,0.014)")
parser.add_argument('--filterByRunInFileName', default=False, action='store_true', help="Filter by run in the name of the files.")
parser.add_argument('--nLSInLumiBlock', default=500, type=int, help="Number of LSs to group for evaluation (Default:  500)")
parser.add_argument('--buildFromScratch', default=1, type=int, help="Start from cert trees (default); do --buildFromScratch=0 to start from \"Before\" histograms")
parser.add_argument('--threshold', default=0.5, type=float, help="The threshold to find active bunches")
parser.add_argument("-t", "--type1byfill", default=False, action='store_true', help="Apply Type 1 Correction by Fill")
args=parser.parse_args()

file = ROOT.TFile.Open(args.inputFile,"READ")
tree = file.Get("LuminosityBlocks")


BXLength=3564
zeroes=array.array('d',[0.]*BXLength)

ROOT.gStyle.SetOptStat(0)

dictRawClustersPerBx={}





a1=0.0#0.06636#0.073827#0.078625#0.076825
a2=0.0
b=0.0#0.00083#0.00078#0.00067#0.00083#0.000811#0.0007891#0.00080518#0.00080518#0.0008125#0.00090625#0.00047
c=0.0#0.0126#0.012#0.017#0.0126#0.012282#0.011867#0.01261#0.0098
b2=0.0
c2=0.0
if args.par!="":
    pars=args.par.split(",")
    if len(pars) >= 3:
        a1=float(pars[0])
        a2=float(pars[1])
        b=float(pars[2])
        c=float(pars[3])
    if len(pars) >= 5:
        b2=float(pars[4])
        c2=float(pars[5])
if args.noType1:
    a1=0
    a2=0
if args.noType2:
    b=0
    b2=0
# Print out the paramters for correction:
print("parameter a1: ", a1)
print("parameter a2: ", a2)
print("parameter b: ", b)
print("parameter c: ", c)
print("parameter b2: ", b2)
print("parameter c2: ", c2)
histpar_a1=ROOT.TH1F("histpar_a1","",10, 0, 10)
histpar_a2=ROOT.TH1F("histpar_a2","",10, 0, 10)
histpar_b=ROOT.TH1F("histpar_b","",10, 0, 10)
histpar_c=ROOT.TH1F("histpar_c","",10, 0, 10)
histpar_b2=ROOT.TH1F("histpar_b2","",10, 0, 10)
histpar_c2=ROOT.TH1F("histpar_c2","",10, 0, 10)
histpar_quad=ROOT.TH1F("histpar_quad","",10, 0, 10)
args.quadTrainCorr=float(args.quadTrainCorr)

for ia1 in range(10):
    histpar_a1.SetBinContent(ia1,a1)
for ia2 in range(10):
    histpar_a2.SetBinContent(ia2,a2)
for ib in range(10):
    histpar_b.SetBinContent(ib,b)
for ic in range(10):
    histpar_c.SetBinContent(ic,c)
for ib2 in range(10):
    histpar_b2.SetBinContent(ib2,b2)
for ic2 in range(10):
    histpar_c2.SetBinContent(ic2,c2)
for iq in range(10):
    histpar_quad.SetBinContent(iq,args.quadTrainCorr)

type2CorrTemplate=ROOT.TH1F("type2CorrTemplate","",BXLength,0,BXLength)

for i in range(1,BXLength):
    type2CorrTemplate.SetBinContent(i,b*exp(-(i-2)*c)+b2*exp(-(i-2)*c2))
type2CorrTemplate.GetXaxis().SetRangeUser(0,100)

for iblock,block in enumerate(tree):
    lumiInfoObj = block.LumiInfo_ALCARECORawPCCProdUnCorr_rawPCCProd_RECO
    #print("bunch 200 clusters ",lumiInfoObj.getInstLumiBX(200))
    dictRawClustersPerBx[str(iblock)]=ROOT.TH1F("RawClustersPerBX_"+str(iblock),"",BXLength,0,BXLength)
    for bx in range(0,BXLength):
        dictRawClustersPerBx[str(iblock)].SetBinContent(bx,lumiInfoObj.getInstLumiBX(bx))
    if iblock==10:
        allLumiPerBX=dictRawClustersPerBx[str(iblock)].Clone()
        noisePerBX=ROOT.TH1F("noisePerBX","",BXLength,0,BXLength)
        corrPerBX=ROOT.TH1F("corrPerBX","",BXLength,0,BXLength)
        corrRatioOverall=ROOT.TH1F("corrRatioOverall","",10,0,10)
        break


canvas = ROOT.TCanvas("c","c",600,600)
canvas.cd()
dictRawClustersPerBx["10"].Draw()
dictRawClustersPerBx["10"].GetXaxis().SetTitle("Bunch Crossing \#")
dictRawClustersPerBx["10"].GetYaxis().SetTitle("Avg. Raw Clusters")
canvas.Draw()
canvas.SaveAs("10th_LS_BX_SBIL.png")

newfile = ROOT.TFile.Open("corrections.root","recreate")
newfile.cd()
#just lumiblock number 10 for now 
allLumiPerBX.SetError(zeroes)
allCorrLumiPerBX=allLumiPerBX.Clone()
allLumiPerBX.SetTitle("Random Triggers in Fill ;BX;Average PCC SBIL Hz/ub")
allCorrLumiPerBX.SetTitle("Random Triggers in Fill , after correction;BX; Average PCC SBIL Hz/ub")
allLumiPerBX.SetLineColor(416)
noise=0

print("Find abort gap")
gap=False
idl=0
num_cut=20
for l in range(1,500):
    if allCorrLumiPerBX.GetBinContent(l)==0 and allCorrLumiPerBX.GetBinContent(l+1)==0 and allCorrLumiPerBX.GetBinContent(l+2)==0:
        gap=True
    if gap and allCorrLumiPerBX.GetBinContent(l)!=0 and idl<num_cut:
        noise+=allCorrLumiPerBX.GetBinContent(l)
        idl+=1

if not idl==0:
    noise=noise/idl
else:
    noise=0
     

print("Apply and save type 1 corrections")

if not args.noType1:
    for k in range(1,BXLength):
        #if not args.type1byfill:
        print("type 1 factor:", a1, a2 )
        bin_k = allLumiPerBX.GetBinContent(k)
        allCorrLumiPerBX.SetBinContent(k+1, allCorrLumiPerBX.GetBinContent(k+1)-bin_k*a1-bin_k*bin_k*a2)
        corrPerBX.SetBinContent(k+1, corrPerBX.GetBinContent(k+1)+bin_k*a1+bin_k*bin_k*a2)

allLumiType1CorrPerBX=allCorrLumiPerBX.Clone()
allLumiType1CorrPerBX.SetError(zeroes)

for m in range(1,BXLength):
    allCorrLumiPerBX.SetBinContent(m, allCorrLumiPerBX.GetBinContent(m)-noise)
    noisePerBX.SetBinContent(m, noise)
    corrPerBX.SetBinContent(m, corrPerBX.GetBinContent(m)+noise)


print("Apply and save type 2 corrections")
if not args.noType2:
    for i in range(1,BXLength):
        for j in range(i+1, i+BXLength):
            binsig_i=allCorrLumiPerBX.GetBinContent(i)
            binfull_i=allLumiPerBX.GetBinContent(i)
            if j<BXLength:
                allCorrLumiPerBX.SetBinContent(j, allCorrLumiPerBX.GetBinContent(j)-binsig_i*type2CorrTemplate.GetBinContent(j-i))
                corrPerBX.SetBinContent(j, corrPerBX.GetBinContent(j)+binsig_i*type2CorrTemplate.GetBinContent(j-i)) 
            else:
                allCorrLumiPerBX.SetBinContent(j-BXLength, allCorrLumiPerBX.GetBinContent(j-BXLength)-binsig_i*type2CorrTemplate.GetBinContent(j-i))
                corrPerBX.SetBinContent(j-BXLength, corrPerBX.GetBinContent(j-BXLength)+binsig_i*type2CorrTemplate.GetBinContent(j-i))

allLumiType1And2CorrPerBX=allCorrLumiPerBX.Clone()
allLumiType1And2CorrPerBX.SetError(zeroes)

print("Apply and save additional quadratic subtraction for trains",args.quadTrainCorr)
if args.quadTrainCorr != 0:
    #find train BXs
    trainBXs=[]
    trainBXs2=[]
    maxBX=0
    for ibx in range(1,BXLength):
        thisSBIL=allCorrLumiPerBX.GetBinContent(ibx)
        if thisSBIL>maxBX:
            maxBX=thisSBIL

    #this ignores the leading bx-desired behavior
    print(maxBX)
    for ibx in range(2,BXLength):
        prevBXActive=(allCorrLumiPerBX.GetBinContent(ibx-1)>maxBX*0.2)
        prevBXActive2=(allCorrLumiPerBX.GetBinContent(ibx-1)>0.5)
        
        if prevBXActive:
            curBXActive=(allCorrLumiPerBX.GetBinContent(ibx)>maxBX*0.2)
            if curBXActive:
                trainBXs.append(ibx)

        if prevBXActive2:
            curBXActive2=(allCorrLumiPerBX.GetBinContent(ibx)>0.5)
            if curBXActive2:
                trainBXs2.append(ibx)

        print(ibx,"prevlumi",allCorrLumiPerBX.GetBinContent(ibx-1),prevBXActive,prevBXActive2,len(trainBXs),len(trainBXs2))
       

    #print LBKey,"trainBXs",len(trainBXs)
    #print LBKey,"trainBXs2",len(trainBXs2)

    for ibx in trainBXs:
        binsig_i=allCorrLumiPerBX.GetBinContent(ibx)
        binfull_i=allLumiPerBX.GetBinContent(ibx)
        allCorrLumiPerBX.SetBinContent(ibx,binsig_i-args.quadTrainCorr*binsig_i*binsig_i)
        corrPerBX.SetBinContent(ibx, corrPerBX.GetBinContent(ibx)+args.quadTrainCorr*binsig_i*binsig_i)
    
activelumi_before = 0
activelumi_after = 0

for ibx in range(1, BXLength):
    if(allCorrLumiPerBX.GetBinContent(ibx)>0.5):
        activelumi_before+=allLumiPerBX.GetBinContent(ibx)
        activelumi_after+=allCorrLumiPerBX.GetBinContent(ibx)
if not activelumi_before==0: 
    corr_ratio=activelumi_after/activelumi_before
else:
    corr_ratio=0

for i in range(1, 10):
    corrRatioOverall.SetBinContent(i, corr_ratio)
print("Finish up dividing plots")

corrRatioPerBX=corrPerBX.Clone()
corrPerBX.SetError(zeroes)
corrRatioPerBX.Divide(allLumiPerBX)
corrRatioPerBX.SetError(zeroes)

noiseToCorrRatio=noisePerBX.Clone()
noiseToCorrRatio.Divide(corrPerBX)
noiseToCorrRatio.SetError(zeroes)

newfile.WriteTObject(allLumiPerBX,  "Before_Corr")
newfile.WriteTObject(allLumiType1CorrPerBX, "After_TypeI_Corr")
newfile.WriteTObject(allLumiType1And2CorrPerBX, "After_TypeI_TypeII_Corr")
newfile.WriteTObject(allCorrLumiPerBX, "After_Corr")
newfile.WriteTObject(noisePerBX, "Noise")
newfile.WriteTObject(corrPerBX, "Overall_Correction")
newfile.WriteTObject(corrRatioPerBX, "Ratio_Correction")
#newfile.WriteTObject(ratio_gap, "Ratio_Nonlumi_"+LBKey)
newfile.WriteTObject(noiseToCorrRatio, "Ratio_Noise")
newfile.WriteTObject(corrRatioOverall, "Overall_Ratio")
