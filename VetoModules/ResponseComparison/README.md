#Instructions for Veto Analysis 
First generate a file list via das client and submit jobs to process the AlCaPCC shown here are for 2018B and 2018D 
```
das_client --query="file dataset=/AlCaLumiPixels/Run2018B-AlCaPCCZeroBias-PromptReco-v*/ALCARECO" > filelistB.txt

python mkAndSubPerModXSEC.py -fl filelistB.txt -s TRUE -d 2018Bjobs

das_client --query="file dataset=/AlCaLumiPixels/Run2018D-AlCaPCCZeroBias-PromptReco-v*/ALCARECO" > filelistD.txt

python mkAndSubPerModXSEC.py -fl filelistD.txt -s TRUE -d 2018Djobs
```
Next, merge the files to produce usable pickle files for the comparison script. You may apply a veto at this step. Although for first iterations I typically don't. Also choose a useful naming scheme for the labels. You'll want to keep track of each permutation.
After merging 
```
python perModuleXSEC_mergeRaw.py -d 2018Bjobs/ --veto veto.txt -l B_veto_1
python perModuleXSEC_mergeRaw.py -d 2018Djobs/ --veto veto.txt -l D_veto_1

python compareTwoModXSECs.py --files output_B_veto_1.pkl,output_D_veto_1.pkl -b 1 -w 0.10 --labels B_D_veto_1,D_B_veto_1 

```
This first veto list is crap we need to inspect the dirstribution so that we can cut correctly:

find the center and make it +- 1% or so ... by eye for now... to automate must fine mean of the fitted gaus and then cut....

CHANGE THE compareTwoModXSECs.py file to reflect this window and rerun to generate the veto list! 
around line 132 - you can see that I've placed all the cuts from the runs in 2018 there ... once changed then rerun. 
```
python compareTwoModXSECs.py --files output_B_veto_1.pkl,output_D_veto_1.pkl -b 1 -w 0.10 --labels B_D_veto_1,D_B_veto_1 

```
next remerge the two datasets with the new veto list! 
```
python perModuleXSEC_mergeRaw.py -d 2018Bjobs/ --veto vetoD_B_veto1.txt -l B_vetoDB_1
python perModuleXSEC_mergeRaw.py -d 2018Djobs/ --veto vetoD_B_veto1.txt -l D_vetoDB_1

```
Then proceed to run the comparison again to check your work
```
python compareTwoModXSECs.py --files output_B_vetoDB_1.pkl,output_D_vetoDB_1.pkl -b 1 -w 0.10 --labels B_D_veto_2,D_B_veto_2 
```
The plots should be narrow and centerd at 1 if the cuts were correct. Then gather this lists from all comparisons to form a master list. In this case the only valid list is vetoD_B_veto1.txt. One may want to do several rounds of cuts. Then to merge I typically do use a quick python script like the following:
```

import pickle
fileBA=open("veto_BA1.txt")
fileCA=open("veto_CA.txt")
fileDA=open("veto_DA.txt")
fileCB=open("veto_CB.txt")
fileDB=open("veto_DB.txt")
fileDC=open("veto_DC1.txt")
modsBA=[]
modsCA=[]
modsDA=[]
modsCB=[]
modsDB=[]
modsDC=[]
for mod in fileBA:
    modsBA.append(int(mod))
for mod in fileCA:
    modsCA.append(int(mod))
for mod in fileDA:
    modsDA.append(int(mod))
for mod in fileCB:
    modsCB.append(int(mod))
for mod in fileDB:
    modsDB.append(int(mod))
for mod in fileDC:
    modsDC.append(int(mod))

setBA=set(modsBA)
setCA=set(modsCA)
setDA=set(modsDA)
setCB=set(modsCB)
setDB=set(modsDB)
setDC=set(modsDC)
setAV=set(modsAV)
setBV=set(modsBV)
setCV=set(modsCV)
setDV=set(modsDV)
mast=open("veto_master_VdM_ABCD.txt","w")
mastlist= list(setBA.union(setCA).union(setDA).union(setCB).union(setDB).union(setDC)) 
mastlist.sort()
for mod in mastlist:
    mast.write(str(mod))
    mast.write("\n")
```

