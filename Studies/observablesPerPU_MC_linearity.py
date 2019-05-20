import ROOT
import sys,os
import numpy
import math

filename=sys.argv[1]
#label=filename.split(".")[0]
label=sys.argv[2]
if not os.path.exists(label):
    os.mkdir(label)
tfile=ROOT.TFile(filename)
tree=tfile.Get("pccminitree")

def MakeResidualPlot(graph,fitFunc):
    myResiduals=ROOT.TGraphErrors()
    Xs=graph.GetX()
    XErrors=graph.GetEX()
    Ys=graph.GetY()
    YErrors=graph.GetEY()

    for iPoint in range(graph.GetN()):
        res=Ys[iPoint]-fitFunc.Eval(Xs[iPoint])
        myResiduals.SetPoint(iPoint, Xs[iPoint],res)
        myResiduals.SetPointError(iPoint, XErrors[iPoint], YErrors[iPoint])

    return myResiduals
        

def GetObs(name):
    obs=-99
    if name is "PCC":
        obs=tree.nCluster
    elif name.find("N. Vertices")!=-1:
        obs=tree.nVtx
    
    return obs



minPU=15
maxPU=50
steps=5

#minPU=30
#maxPU=32
#steps=1

maxBin=210
#int(maxPU+math.sqrt(maxPU)*2)

can=ROOT.TCanvas("can","",1000,700)


means=[]
means=[0.3,0.5,1,2,3,4,5,6,8,9,10,11,12]
for imean in numpy.arange(minPU,maxPU+0.01,steps):
    means.append(imean)
print means




observables={}

observables["PCC"]=[tree.nCluster,750,15000]
observables["N. Vertices"]=[tree.nVtx,maxBin,maxBin]



for observable in observables.keys():
    observables[observable].append(ROOT.TGraphErrors())
    observables[observable][-1].SetTitle(";Average Pile-up;Average "+observable)
    observables[observable].append(ROOT.TGraphErrors())
    observables[observable][-1].SetTitle(";Average Pile-up;Average "+observable+"/Average Pile-up")
    counters={}
    for mean in means:
        counters[mean]=ROOT.TH1F(observable+"s"+str(mean),";"+observable+" with average pile-up of "+str(mean),observables[observable][1],0,observables[observable][2])
    observables[observable].append(counters)



iGraph=0
reweighting={}
newtarget={}
checkpileup={}

simText=ROOT.TLatex(.15,.9,"CMS #it{Simulation Preliminary}")
simText.SetNDC(ROOT.kTRUE)


pileup=ROOT.TH1F("pileup","Pile-up",maxBin,0,maxBin)
tree.Draw("nPU>>pileup")
can.Update()
can.SaveAs("originalPU.png")
pileup.Scale(1/pileup.Integral())
for mean in means:
    newtarget[mean]=pileup.Clone("newtarget"+str(mean))
    newtarget[mean].SetTitle("target PU (mean="+str(mean)+")")
    checkpileup[mean]=ROOT.TH1F("checkpileup","PU after re-weight (mean="+str(mean)+")",maxBin,0,maxBin)
    last5PercentBin=0
    last2PercentBin=0
    last1PercentBin=0
    for ibin in range(0,newtarget[mean].GetNbinsX()+1):
        newtarget[mean].SetBinContent(ibin+1,ROOT.TMath.PoissonI(ibin,mean))
        #if ibin<30:
        #    print ibin,newtarget.GetBinContent(ibin+1)
        if ROOT.TMath.PoissonI(ibin,mean) > 0.05:
            last5PercentBin=ibin
        if ROOT.TMath.PoissonI(ibin,mean) > 0.02:
            last2PercentBin=ibin
        if ROOT.TMath.PoissonI(ibin,mean) > 0.01:
            last1PercentBin=ibin

    binsWithLast1Percent=0
    for ibin in range(0,newtarget[mean].GetNbinsX()):
        if newtarget[mean].Integral(ibin,newtarget[mean].GetNbinsX()) > 0.01:
            binsWithLast1Percent=ibin
    print "mean,last1PercentBin,binsWithLast1Percent",mean,last1PercentBin,binsWithLast1Percent
    newtarget[mean].Scale(1/newtarget[mean].Integral())
    newtarget[mean].Draw()
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/targetPU_mean"+str(mean)+".png")
    #raw_input()       

    reweighting[mean]=newtarget[mean].Clone("ratio")
    reweighting[mean].Divide(pileup)
    reweighting[mean].SetTitle("reweighting")
    #print "Integral,bin0,1,2,3,",reweighting[mean].Integral(),reweighting[mean].GetBinContent(0),reweighting[mean].GetBinContent(1),reweighting[mean].GetBinContent(2),reweighting[mean].GetBinContent(3)
    reweighting[mean].Draw()
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/PUreweighting_mean"+str(mean)+".png")


nentries=tree.GetEntries()
print nentries
for iev in range(nentries):
    tree.GetEntry(iev)
    if iev%10000==0:
        print "iev,",iev,
        for observable in observables.keys():
            print observable,GetObs(observable),
        print

    for mean in means:
        for observable in observables.keys():
            observables[observable][5][mean].Fill(GetObs(observable),reweighting[mean].GetBinContent(int(tree.nPU)+1))
            # am I getting the right value?

        checkpileup[mean].Fill(tree.nPU,reweighting[mean].GetBinContent(int(tree.nPU)+1))
    

for mean in means:
    #print iGraph, imean, PCCs[mean].GetMean(),checkpileup[mean].GetMeanError(), PCCs[mean].GetMeanError()


    checkpileup[mean].Scale(1./checkpileup[mean].Integral())

    #need observables loop
    for observable in observables.keys():
        observables[observable][3].SetPoint(iGraph, mean, observables[observable][5][mean].GetMean())
        observables[observable][3].SetPointError(iGraph, checkpileup[mean].GetMeanError(), observables[observable][5][mean].GetMeanError())
        observables[observable][4].SetPoint(iGraph, mean, observables[observable][5][mean].GetMean()/mean)
        observables[observable][4].SetPointError(iGraph, checkpileup[mean].GetMeanError(), observables[observable][5][mean].GetMeanError()/mean)
        observables[observable][5][mean].Draw("hist")
        simText.Draw("same")
        can.Update()
        if mean==45.0:
            can.SaveAs(label+"/"+observable+"_PU"+str(mean).replace(".","_")+".png")
            can.SaveAs(label+"/"+observable+"_PU"+str(mean).replace(".","_")+".pdf")
            can.SaveAs(label+"/"+observable+"_PU"+str(mean).replace(".","_")+".C")

    leg=ROOT.TLegend(0.5,0.7,0.95,0.95)
    checkpileup[mean].SetLineColor(1)
    checkpileup[mean].SetLineWidth(2)
    checkpileup[mean].Draw()
    newtarget[mean].SetLineColor(600)
    newtarget[mean].SetLineWidth(2)
    newtarget[mean].Draw("same")
    leg.AddEntry(checkpileup[mean],"Re-weighted PU","l")
    leg.AddEntry(newtarget[mean],"Target PU","l")
    leg.Draw()
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/reweightingCheck_PU"+str(mean)+".png")
    #raw_input()
    
    iGraph=iGraph+1
    

line=ROOT.TF1("line","pol1",means[0]*0.9,means[-1]*1.03)
xOverNPU=ROOT.TF1("xOverNPU","[0]+[1]/x",means[0]*0.9,means[-1]*1.03)
iPlot=0

for observable in observables.keys():
    observables[observable][3].Draw("AP")
    fitRes=observables[observable][3].Fit(line,"S")
    realMaxPU=max(means)
    fitErrorGraph=ROOT.TGraphErrors()
    fitErrorGraph.SetFillStyle(3002)
    fitErrorGraph.SetFillColor(633)

    for iPoint in range(100):
        thisPU=(iPoint+0.01)/100. * realMaxPU
        fitErrorGraph.SetPoint(iPoint,thisPU,line.Eval(thisPU))
        fitErrorGraph.SetPointError(iPoint,0,line.IntegralError(thisPU-1,thisPU+1)/(2))
        print iPoint,line.IntegralError(thisPU-1,thisPU+1)/2,thisPU

    leg=ROOT.TLegend(0.45,0.45,0.87,0.15) 
    leg.AddEntry(line,observable+"/nPU = "+"{:.2f} #pm {:.2f}".format(fitRes.Parameter(1),fitRes.ParError(1)),"l")
    #leg.AddEntry(line,"noise "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(0),fitRes.ParError(0)),"l")
    leg.AddEntry(line,"#chi^{2}/NDF = "+"{:.1f} / {:.1f}".format(fitRes.Chi2(),fitRes.Ndf()),"l")
    leg.Draw("same")
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/"+observable+str(iPlot)+"vsPU.png")
    can.SaveAs(label+"/"+observable+str(iPlot)+"vsPU.pdf")
    can.SaveAs(label+"/"+observable+str(iPlot)+"vsPU.root")
    can.SaveAs(label+"/"+observable+str(iPlot)+"vsPU.C")
    #raw_input()

    iPlot=iPlot+1
    residual=MakeResidualPlot(observables[observable][3],line)
    residual.SetTitle(";nPU;#Delta"+observable+"_{MC-Fit}")
    residual.Draw("APE")
    #fitErrorGraph.Draw("same")
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/"+str(iPlot)+observable+"ResidualsvsPU.png")
    iPlot=iPlot+1
    

    observables[observable][4].Draw("AP")
    if observable is "PCC":
        fitRes=observables[observable][4].Fit(xOverNPU,"S")
        leg=ROOT.TLegend(0.35,0.45,0.87,0.85) 
        leg.AddEntry(xOverNPU,observable+"/nPU = "+"{:.2f} #pm {:.2f}".format(fitRes.Parameter(0),fitRes.ParError(0)),"l")
        leg.AddEntry(xOverNPU,"Constant = "+"{:.2f} #pm {:.2f}".format(fitRes.Parameter(1),fitRes.ParError(1)),"l")
        leg.AddEntry(xOverNPU,"#chi^{2}/NDF = "+"{:.1f} / {:.1f}".format(fitRes.Chi2(),fitRes.Ndf()),"l")
        leg.Draw("same")
    simText.Draw("same")
    can.Update()
    can.SaveAs(label+"/"+observable+str(iPlot)+"vsPU.png")
    iPlot=iPlot+1
    #raw_input()


