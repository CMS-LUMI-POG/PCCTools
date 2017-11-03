import ROOT
import sys,os
import numpy
import math

filename=sys.argv[1]
label=filename.split(".")[0]
if not os.path.exists(label):
    os.mkdir(label)
tfile=ROOT.TFile(filename)
tree=tfile.Get("pccminitree")


minPU=15
maxPU=51
steps=5

#minPU=30
#maxPU=32
#steps=5

maxBin=100
#int(maxPU+math.sqrt(maxPU)*2)

can=ROOT.TCanvas("can","",1100,600)

tgraph=ROOT.TGraphErrors()
tgraph.SetTitle(";Average PU; Average PCC")

vtx_tgraph=ROOT.TGraphErrors()
#vtx_tgraph.SetTitle(";Average PU; Average Tight nVtx")
vtx_tgraph.SetTitle(";Average PU; Average Inclusive nVtx")
iGraph=0
reweighting={}
newtarget={}
PCCs={}
nVtxs={}
checkpileup={}

doPoissonTest=True
output=open("poissonTests_min"+str(minPU)+"_max"+str(maxPU)+".txt","w")
output.write("PUmean,averageGoodMean,ratio,r_err\n")
if doPoissonTest:
    line=ROOT.TF1("line","pol1",0.5,20)
    means=[]
    means=[0.1,0.2,0.3,0.5,1,2,3,4,5,6,8,9,10,11,12]
    for imean in numpy.arange(minPU,maxPU+0.01,steps):
        means.append(imean)
    print means
    iMean=1
    pileup=ROOT.TH1F("pileup","Pile-up",100,0,100)
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
    
    
        PCCs[mean]=ROOT.TH1F("PCCs"+str(mean),";PCC",10000,0,40000)
        nVtxs[mean]=ROOT.TH1F("nVtxs"+str(mean),";nVtx",100,0,100)
    
    nentries=tree.GetEntries()
    print nentries
    for iev in range(nentries):
        tree.GetEntry(iev)
        if iev%1000==0:
            print "iev,nVtx",iev,tree.nVtx
        for mean in means:
            PCCs[mean].Fill(tree.nCluster,reweighting[mean].GetBinContent(int(tree.nPU)+1))
            nVtxs[mean].Fill(tree.nVtx,reweighting[mean].GetBinContent(int(tree.nPU)+1))

            checkpileup[mean].Fill(tree.nPU,reweighting[mean].GetBinContent(int(tree.nPU)+1))
        
        output.write(str(mean)+","+str(PCCs[mean].GetMean())+","+str(PCCs[mean].GetMean()/mean)+","+str(PCCs[mean].GetMeanError()/mean)+"\n")
        
    for mean in means:
        tgraph.SetPoint(iGraph, mean, PCCs[mean].GetMean())
        tgraph.SetPointError(iGraph, checkpileup[mean].GetMeanError(), PCCs[mean].GetMeanError())
        vtx_tgraph.SetPoint(iGraph, mean, nVtxs[mean].GetMean())
        vtx_tgraph.SetPointError(iGraph, checkpileup[mean].GetMeanError(), nVtxs[mean].GetMeanError())
        #print iGraph, imean, PCCs[mean].GetMean(),checkpileup[mean].GetMeanError(), PCCs[mean].GetMeanError()

        iGraph=iGraph+1

        #for ibin in range(20):
        ##for ibin in range(checkpileup.GetNbinsX()):
        #    print ibin,
        #    if newtarget.GetBinContent(ibin)>0:
        #        print checkpileup.GetBinContent(ibin)/newtarget.GetBinContent(ibin),checkpileup.GetBinContent(ibin),newtarget.GetBinContent(ibin)
        #        checkpileup.SetBinContent(ibin,checkpileup.GetBinContent(ibin)/newtarget.GetBinContent(ibin))
        checkpileup[mean].Scale(1./checkpileup[mean].Integral())
        #checkpileup[mean].Draw("hist")
        #can.Update()
        #can.SaveAs(label+"/reweightedPU_PU"+str(mean)+".png")
        #raw_input()
    
    
        PCCs[mean].Draw("hist")
        can.Update()
        can.SaveAs(label+"/PCC_PU"+str(mean)+".png")
        #raw_input()
        
        nVtxs[mean].Draw("hist")
        can.Update()
        can.SaveAs(label+"/nVtx_PU"+str(mean)+".png")
        #raw_input()

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
    

output.close()
tgraph.Draw("AP")
tgraph.Fit("pol1")
can.Update()
can.SaveAs(label+"/PCCvsPU.png")
#raw_input()

vtx_tgraph.Draw("AP")
vtx_tgraph.SetMaximum(50)
vtx_tgraph.SetMinimum(0.01)
can.SetLogx()
can.SetLogy()
vtx_tgraph.Fit("pol1")
can.Update()
can.SaveAs(label+"/nVtxvsPU.png")
#raw_input()

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
