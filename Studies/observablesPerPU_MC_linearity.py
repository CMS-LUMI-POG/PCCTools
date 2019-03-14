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
    elif name is "Vtx":
        obs=tree.nVtx
    
    return obs



minPU=15
maxPU=75
steps=5

#minPU=30
#maxPU=32
#steps=1

maxBin=210
#int(maxPU+math.sqrt(maxPU)*2)

can=ROOT.TCanvas("can","",1100,600)


means=[]
means=[0.1,0.2,0.3,0.5,1,2,3,4,5,6,8,9,10,11,12,140]
for imean in numpy.arange(minPU,maxPU+0.01,steps):
    means.append(imean)
print means




observables={}

observables["PCC"]=[tree.nCluster,10000,20000]
observables["Vtx"]=[tree.nVtx,maxBin,maxBin]



for observable in observables.keys():
    observables[observable].append(ROOT.TGraphErrors())
    observables[observable][-1].SetTitle(";Average PU; Average "+observable)
    observables[observable].append(ROOT.TGraphErrors())
    observables[observable][-1].SetTitle(";Average PU; MC - Fit "+observable)
    counters={}
    for mean in means:
        counters[mean]=ROOT.TH1F(observable+"s"+str(mean),";"+observable,observables[observable][1],0,observables[observable][2])
    observables[observable].append(counters)



iGraph=0
reweighting={}
newtarget={}
checkpileup={}


iMean=1
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
    can.Update()
    can.SaveAs(label+"/targetPU_mean"+str(mean)+".png")
    #raw_input()       

    reweighting[mean]=newtarget[mean].Clone("ratio")
    reweighting[mean].Divide(pileup)
    reweighting[mean].SetTitle("reweighting")
    #print "Integral,bin0,1,2,3,",reweighting[mean].Integral(),reweighting[mean].GetBinContent(0),reweighting[mean].GetBinContent(1),reweighting[mean].GetBinContent(2),reweighting[mean].GetBinContent(3)
    reweighting[mean].Draw()
    can.Update()
    can.SaveAs(label+"/PUreweighting_mean"+str(mean)+".png")


nentries=tree.GetEntries()
print nentries
for iev in range(nentries):
    tree.GetEntry(iev)
    if iev%1000==0:
        print "iev,nVtx",iev,
        for observable in observables.keys():
            print GetObs(observable)
        print

    for mean in means:
        for observable in observables.keys():
            observables[observable][5][mean].Fill(GetObs(observable),reweighting[mean].GetBinContent(int(tree.nPU)+1))
            # am I getting the right value?

        checkpileup[mean].Fill(tree.nPU,reweighting[mean].GetBinContent(int(tree.nPU)+1))
    

for mean in means:
    #print iGraph, imean, PCCs[mean].GetMean(),checkpileup[mean].GetMeanError(), PCCs[mean].GetMeanError()

    iGraph=iGraph+1

    checkpileup[mean].Scale(1./checkpileup[mean].Integral())

    #need observables loop
    for observable in observables.keys():
        observables[observable][3].SetPoint(iGraph, mean, observables[observable][5][mean].GetMean())
        observables[observable][3].SetPointError(iGraph, checkpileup[mean].GetMeanError(), observables[observable][5][mean].GetMeanError())
        observables[observable][4].SetPoint(iGraph, mean, observables[observable][5][mean].GetMean()/mean)
        observables[observable][4].SetPointError(iGraph, checkpileup[mean].GetMeanError(), observables[observable][5][mean].GetMeanError()/mean)
        observables[observable][5][mean].Draw("hist")
        can.Update()
        can.SaveAs(label+"/"+observable+"_PU"+str(mean)+".png")

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
    can.Update()
    can.SaveAs(label+"/reweightingCheck_PU"+str(mean)+".png")
    #raw_input()
    

line=ROOT.TF1("line","pol1",means[0]*0.9,means[-1]*1.03)
xOverNPU=ROOT.TF1("xOverNPU","[0]+[1]/x",means[0]*0.9,means[-1]*1.03)
iPlot=0
for observable in observables.keys():
    observables[observable][3].Draw("AP")
    fitRes=observables[observable][3].Fit(line,"S")
    leg=ROOT.TLegend(0.55,0.45,0.87,0.15) 
    leg.AddEntry(line,"slope "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(1),fitRes.ParError(1)),"l")
    leg.AddEntry(line,"noise "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(0),fitRes.ParError(0)),"l")
    leg.AddEntry(line,"chi2/ndf "+"{:.4f} / {:.4f}".format(fitRes.Chi2(),fitRes.Ndf()),"l")
    leg.Draw("same")
    can.Update()
    can.SaveAs(label+"/"+str(iPlot)+observable+"vsPU.png")
    #raw_input()

    iPlot=iPlot+1
    residual=MakeResidualPlot(observables[observable][3],line)
    residual.SetTitle(";nPU;#Delta"+observable+"_{MC-Fit}")
    residual.Draw("APE")
    can.Update()
    can.SaveAs(label+"/"+str(iPlot)+observable+"ResidualsvsPU.png")
    iPlot=iPlot+1
    

    observables[observable][4].Draw("AP")
    fitRes=observables[observable][4].Fit(xOverNPU,"S")
    leg=ROOT.TLegend(0.55,0.45,0.87,0.15) 
    leg.AddEntry(line,"slope "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(1),fitRes.ParError(1)),"l")
    leg.AddEntry(line,"noise "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(0),fitRes.ParError(0)),"l")
    leg.AddEntry(line,"chi2/ndf "+"{:.4f} / {:.4f}".format(fitRes.Chi2(),fitRes.Ndf()),"l")
    leg.Draw("same")
    can.Update()
    can.SaveAs(label+"/"+str(iPlot)+observable+"vsPU.png")
    iPlot=iPlot+1
    #raw_input()


#pccConst=fitRes.Parameter(0) #-2*fitRes.ParError(0)
#pccConstError=fitRes.ParError(0)
#thesePU=tgraph.GetX()
#thesePUError=tgraph.GetEX()
#thesePCC=tgraph.GetY()
#thesePCCError=tgraph.GetEY()
#
#for iPoint in range(tgraph.GetN()):
#    tgraph.SetPoint(iPoint,thesePU[iPoint],(thesePCC[iPoint]-pccConst)/thesePU[iPoint])
#    tgraph.SetPointError(iPoint,thesePUError[iPoint],math.sqrt(thesePCCError[iPoint]**2+pccConstError**2)/thesePU[iPoint])
#
#fitRes=tgraph.Fit(line,"S")
#legpcc=ROOT.TLegend(0.55,0.85,0.87,0.55) 
#legpcc.AddEntry(line,"slope "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(1),fitRes.ParError(1)),"l")
#legpcc.AddEntry(line,"const "+"{:.4f} #pm {:.4f}".format(fitRes.Parameter(0),fitRes.ParError(0)),"l")
#legpcc.AddEntry(line,"chi2/ndf "+"{:.4f} / {:.4f}".format(fitRes.Chi2(),fitRes.Ndf()),"l")
#tgraph.Draw("APE")
#legpcc.Draw("same")
#can.Update()
#can.SaveAs(label+"/3PCCOverNPUvsPU.png")
##raw_input()



####change fit model for vertex counting
###vtx_tgraph.Draw("AP")
###vtx_tgraph.SetMaximum(50)
###vtx_tgraph.SetMinimum(0.01)
####can.SetLogx()
####can.SetLogy()
###line2=ROOT.TF1("line2","pol1",means[0]*0.9,means[-1]*1.03)
###vtxFitRes=vtx_tgraph.Fit(line2,"S")
###legVtx=ROOT.TLegend(0.55,0.85,0.87,0.55) 
###legVtx.AddEntry(line2,"slope "+"{:.4f} #pm {:.4f}".format(vtxFitRes.Parameter(1),vtxFitRes.ParError(1)),"l")
###legVtx.AddEntry(line2,"noise "+"{:.4f} #pm {:.4f}".format(vtxFitRes.Parameter(0),vtxFitRes.ParError(0)),"l")
###legVtx.AddEntry(line2,"chi2/ndf "+"{:.4f} / {:.4f}".format(vtxFitRes.Chi2(),vtxFitRes.Ndf()),"l")
###legVtx.Draw("same")
###can.Update()
###can.SaveAs(label+"/4nVtxvsPU.png")
####raw_input()
###
###vtxResidual=MakeResidualPlot(vtx_tgraph,line2)
###vtxResidual.SetTitle("Vertex Counting Residuals;nPU;#DeltaVertices_{MC-Fit}")
###vtxResidual.Draw("APE")
###can.Update()
###can.SaveAs(label+"/5nVtxResidualsvsPU.png")
###
###
###thesePU=vtx_tgraph.GetX()
###thesePUError=vtx_tgraph.GetEX()
###theseVTX=vtx_tgraph.GetY()
###theseVTXError=vtx_tgraph.GetEY()
###
###for iPoint in range(vtx_tgraph.GetN()):
###    vtx_tgraph.SetPoint(iPoint,thesePU[iPoint],(theseVTX[iPoint])/thesePU[iPoint])
###    vtx_tgraph.SetPointError(iPoint,thesePUError[iPoint],theseVTXError[iPoint]/thesePU[iPoint])
###
###vtx_tgraph.Draw("AP")
###vtx_tgraph.SetMaximum(0.5)
###vtx_tgraph.SetMinimum(0.3)
###vtxFitRes=vtx_tgraph.Fit(line2,"S")
###legvtx=ROOT.TLegend(0.55,0.45,0.87,0.15) 
###legvtx.AddEntry(line2,"slope "+"{:.4f} #pm {:.4f}".format(vtxFitRes.Parameter(1),vtxFitRes.ParError(1)),"l")
###legvtx.AddEntry(line2,"const "+"{:.4f} #pm {:.4f}".format(vtxFitRes.Parameter(0),vtxFitRes.ParError(0)),"l")
###legvtx.AddEntry(line2,"chi2/ndf "+"{:.4f} / {:.4f}".format(vtxFitRes.Chi2(),vtxFitRes.Ndf()),"l")
###legvtx.Draw("same")
###can.Update()
###can.SaveAs(label+"/6nVtxOverNPUvsPU.png")
####raw_input()

sys.exit(0)


newfile=open("output.txt","w")

cutmax=10
fitmin=minPU+0.5
fitmax=maxPU+0.5

hists={}
fits={}

hists["2d"]=ROOT.TH2F("2d","#chi^{2}/NDoF for Linear Fits at Numerous Test Points;NDoF Cut; Max Fit Range",cutmax+1,-1,cutmax,int(fitmax),0,int(fitmax))
newfile.write("icut,imax,chi2/ndf,chi2,ndf,p0,p1\n")
for icut in range(-1,cutmax):
    histkey="cut"+str(icut)
    hists[histkey]=ROOT.TProfile(histkey,";Number of Selected Vertices;Average number of pile-up",maxPU*2+1,-0.25,maxPU+0.25)
    cutstr="Sum$(vtx_ndof>"+str(icut)+" && vtx_isValid && !vtx_isFake)"
    tree.Draw("nPU:"+cutstr+">>"+histkey,"","profile")
    
    hists[histkey].Draw()
   
    textbox=ROOT.TPaveText(0.12,0.5,0.4,0.88,"NDC")
    textbox.SetFillColor(ROOT.kWhite)
    textbox.SetLineColor(ROOT.kBlack)
    textbox.AddText("Vertex Selection:")
    textbox.AddText("NDoF>"+str(icut)+", isValid,")
    textbox.AddText("and not isFake")
    textbox.AddLine(.0,.5,1.,.5)
    textbox.AddText("#chi^{2}/NDof  < 2:  Green")
    textbox.AddText("#chi^{2}/NDof 2-15:  Yellow")
    textbox.AddText("#chi^{2}/NDof > 15:  Red")

    textbox.Draw("same")
 
    for imax in reversed(range(int(fitmin+3),int(fitmax))):
        fitkey="cut"+str(icut)+"_max"+str(imax)
        fits[fitkey]=ROOT.TF1(fitkey,"pol1",fitmin,imax+0.5)
        hists[histkey].Fit(fits[fitkey],"","",fitmin,imax+0.5)
   
        if fits[fitkey].GetNDF() > 0: 
            newfile.write(str(icut)+","+str(imax)+","+str(fits[fitkey].GetChisquare()/fits[fitkey].GetNDF())+","+str(fits[fitkey].GetChisquare())+","+str(fits[fitkey].GetNDF())+","+str(fits[fitkey].GetParameter(0))+","+str(fits[fitkey].GetParameter(1))+"\n")
            hists["2d"].Fill(icut,imax,fits[fitkey].GetChisquare()/fits[fitkey].GetNDF())
            if fits[fitkey].GetChisquare()/fits[fitkey].GetNDF() < 2:
                fits[fitkey].SetLineColor(ROOT.kGreen)
                fits[fitkey].SetLineWidth(3)
            elif fits[fitkey].GetChisquare()/fits[fitkey].GetNDF() < 15:
                fits[fitkey].SetLineColor(ROOT.kYellow)
                fits[fitkey].SetLineWidth(2)
            else:
                fits[fitkey].SetLineColor(ROOT.kRed)
                fits[fitkey].SetLineWidth(1)
            fits[fitkey].SetLineStyle(2)
            
            fits[fitkey].Draw("sames")
        
 
    can.Update()
    #raw_input()
#    can.SaveAs("nvtx_vs_pu_"+histkey+".png")

hists["2d"].SetMaximum(100)
hists["2d"].Draw("colz")
can.SetLogz()
can.Update()
#can.SaveAs("normalizedchi2_results.png")

#raw_input()
newfile.close()
