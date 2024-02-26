
#include "fitAfterglowTrain.C"

#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <vector>
#include <string>
#include <utility>
#include <map>
#include <boost/program_options.hpp>
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TTree.h"
#include "TObject.h"
#include "TChain.h"
#include "TFile.h"
#include "TF1.h"
#include "TMath.h"
#include "TSystem.h"
#include "TPaveText.h"
#include "TPave.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TRandom.h"
#include "TLorentzVector.h"
#include "TRandom3.h"
#include <TROOT.h>

#include "time.h"
#include "RooDataHist.h"
#include "RooDataSet.h"
#include "RooAbsPdf.h"
#include "RooGaussian.h"
#include "RooGaussModel.h"
#include "RooAddModel.h"
#include "RooVoigtian.h"
#include "RooFitResult.h"
#include "RooBernstein.h"
#include "RooPolynomial.h"
#include "RooAddPdf.h"
#include "RooRealVar.h"
#include "RooFormulaVar.h"
#include "RooArgList.h"
#include "RooWorkspace.h"
#include "RooMsgService.h"
#include "RooMinuit.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGaxis.h"
#include "TString.h"
#include "TList.h"
#include "TAxis.h"
#include "TAxis.h"
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <cstring>
#include <stdlib.h>
#include <TMath.h>
#include <TChain.h>
#include <TFile.h>

#include "TFitResult.h"
#include "TLatex.h"
#include "TVirtualFitter.h"
#include "TObject.h"
#include "TObjString.h"

//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={366800}, std::vector<int> LeadBCIDList={1113,1575,2007,2901}, int NCOLLIDINGBCIDS=36, int NTOTALBCIDS=100){


///////////////
//  2018 data
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995,320996}, std::vector<int> LeadBCIDList={1}, int NCOLLIDINGBCIDS=11, int NTOTALBCIDS=100){//1-wagon
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995,320996}, std::vector<int> LeadBCIDList={188,1070,1964,2858}, int NCOLLIDINGBCIDS=103, int NTOTALBCIDS=200){//2-wagons
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995}, std::vector<int> LeadBCIDList={188}, int NCOLLIDINGBCIDS=103, int NTOTALBCIDS=200){
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995,320996}, std::vector<int> LeadBCIDList={454,1336,2230,3124}, int NCOLLIDINGBCIDS=158, int NTOTALBCIDS=240){//3-wagons
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995,320996}, std::vector<int> LeadBCIDList={1336}, int NCOLLIDINGBCIDS=158, int NTOTALBCIDS=240){//3-wagons
//void fitAfterglowRun(TString inpath=".", std::vector<int> RunList={320995}, std::vector<int> LeadBCIDList={3124}, int NCOLLIDINGBCIDS=158, int NTOTALBCIDS=240){


///////////////
///    2022 Data
//std::vector<int> RunList={361948}; std::vector<int> LeadBCIDList={1018,2806}; int NCOLLIDINGBCIDS=189; int NTOTALBCIDS=250; //600b fill 8383 -> few blocks

//Jose's last one
//std::vector<int> RunList={360991}; std::vector<int> LeadBCIDList={1018,2806}; int NCOLLIDINGBCIDS=189; int NTOTALBCIDS=250; //600b Fill 8307  

//std::vector<int> RunList={361957}; std::vector<int> LeadBCIDList={66,2748}; int NCOLLIDINGBCIDS=208; int NTOTALBCIDS=270;//1800b fill 8385 -> mu scan fill, fit smooth part


//Sam try
//std::vector<int> RunList={369978}; std::vector<int> LeadBCIDList={1001,1894}; int NCOLLIDINGBCIDS=236; int NTOTALBCIDS=295; //600b Fill 8307  
//for this run we will stop at 200 bcid...
//std::vector<int> RunList={369978}; std::vector<int> LeadBCIDList={1001,1894}; int NCOLLIDINGBCIDS=236; int NTOTALBCIDS=295; //600b Fill 8307  

    
std::vector<int> RunList={366442}; 
std::vector<int> LeadBCIDList={1}; 
int NCOLLIDINGBCIDS=1; 
int NTOTALBCIDS=51; //3b Fill 8637
//std::vector<int> RunList={366442}; std::vector<int> LeadBCIDList={1,1786}; int NCOLLIDINGBCIDS=2; int NTOTALBCIDS=100; //3b Fill 8637

// nice run but long 
//std::vector<int> RunList={369998}; std::vector<int> LeadBCIDList={2215,2258,2301,2344,2387}; int NCOLLIDINGBCIDS=179; int NTOTALBCIDS=300; 
//std::vector<int> RunList={369998}; 
//std::vector<int> LeadBCIDList=
//    {1802,1814,1826,1838,1850,1862,1874,//+12
//        1889,1932,1975,2018,2061,//+43
//        2128,2140,2152,2164,2176,2188,2200,//+12
//        2215,2258,2301,2344,2387}; //+43
//int NCOLLIDINGBCIDS=598; 
//int NTOTALBCIDS=800;

//not correct because of the lack of abort gap
//std::vector<int> RunList={369998}; std::vector<int> LeadBCIDList={2215}; int NCOLLIDINGBCIDS=215; int NTOTALBCIDS=300; 

//std::vector<int> RunList={369998}; 
//std::vector<int> LeadBCIDList=
//  //{1802,1814,1826,1838,1850,1862,1874,//+12
//        //1889,1932,1975,2018,2061,//+43
//        {2128,2140,2152,2164,2176,2188,2200,//+12
//        2215,2258,2301,2344,2387}; //+43
//int NCOLLIDINGBCIDS=299; 
//int NTOTALBCIDS=359;

//std::vector<int> RunList={369998}; 
//std::vector<int> LeadBCIDList=
//  {1802,1814,1826,1838,1850,1862,1874,//+12
//        1889,1932,1975,2018,2061,//+43
//        2128,2140,2152,2164,2176,2188,2200,//+12
//        2215,2258,2301,2344,2387}; //+43
//int NCOLLIDINGBCIDS=598; 
//int NTOTALBCIDS=805;
//int NCOLLIDINGBCIDS=621; 
//int NTOTALBCIDS=675;

//std::vector<int> RunList={366793}; std::vector<int> LeadBCIDList={2470}; int NCOLLIDINGBCIDS=35; int NTOTALBCIDS=85; 
//std::vector<int> RunList={366801}; 
//std::vector<int> LeadBCIDList=
//    //2902 is a candidate but doesn't have 3rd wagon
//    //{682,1576,2470,3041}; //third
//    {220,1114,2008,2902}; //first wagon
//
////int NCOLLIDINGBCIDS=385; //total
//int NCOLLIDINGBCIDS=36; //total
//int NTOTALBCIDS=86; 

//std::vector<int> RunList={369978}; 
//std::vector<int> LeadBCIDList=
//    {1895,2820}; 
//
////int NCOLLIDINGBCIDS=385; //total
////int NCOLLIDINGBCIDS=236; //total INCLUDE GAPS?!
//int NCOLLIDINGBCIDS=295; //total INCLUDE GAPS?!
//int NTOTALBCIDS=345; 

//hmmm first train then second 24 35 


//////////////////////////////////////////////
void fitAfterglowRun(TString inpath=""){

  if(inpath.CompareTo("")==0) return;

  
  TString OutfileName=inpath+"/fitAfterglow_output.root";
  TFile outputfile(OutfileName,"recreate");
  
  gROOT->cd();
  makeTree();
  

  for(int r=0;r<RunList.size();r++){
  
    TFile File((inpath+"/"+RunList[r]+".root").Data(),"read");
    if(File.IsZombie()){
      cout<<(inpath+"/"+RunList[r]).Data()<<" not found"<<endl;
      return;
    }
  
    TIter next(File.GetListOfKeys());
    //for reading out the lumiinfo object 
    //LumiInfo_ALCARECORawPCCProdUnCorr_rawPCCProd_RECO.obj.instLumiByBX_
    
    while (TObject* key = next()) {
      TString kname(key->GetName());
      if(!kname.Contains("RawLumiAvg")) continue;
      //if(!LumiInfo_ALCARECORawPCCProdUnCorr_rawPCCProd_RECO

      cout<<key->GetName()<<endl;

      TH1F* H=(TH1F*)File.Get(key->GetName());
    
      for(int i=0;i<LeadBCIDList.size();i++)
	fitAfterglowTrain(H,key->GetName(), LeadBCIDList[i], NCOLLIDINGBCIDS, NTOTALBCIDS,inpath);


    }

  }

  
  outputfile.cd();
  if(Tree) Tree->Write();
  outputfile.ls();
  outputfile.Close();
  
}
