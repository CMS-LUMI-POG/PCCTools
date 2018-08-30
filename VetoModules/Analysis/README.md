#Instructions for Veto Analysis 
First generate a file list via das client:
```
das_client --query="file dataset=/AlCaLumiPixels/Run2018B-AlCaPCCRandom-PromptReco-v*/ALCARECO" > filelist.txt

python mkAndSubPerModXSEC.py -fl filelist2018DZB.txt -s TRUE -d 2018Djobs

python perModuleXSEC_mergeRaw.py -d 2018Bjobs/ --veto vetoAB_llB.txt -l vetoAB_llB_B

python compareTwoModXSECs.py --files output_vetoAB_llB.pkl,output_vetoAB_llB_B.pkl -b 1 -w 0.10 --labels A_lostlistB_1,B_lostlistB_1 --vetoList vetoAB_llB.txt
```
find the center and make it +- 1% or so ... by eye for now... to automate must fine mean of the fitted gaus and then cut.... 

CHANGE THE compareTwoModXSECs.py file to reflect this window and rerun to generate the veto list! 
```
python compareTwoModXSECs.py --files output_vetoAB_llB.pkl,output_vetoAB_llB_B.pkl -b 1 -w 0.10 --labels A_lostlistB_1,B_lostlistB_1 --vetoList vetoAB_llB.txt
```
next remerge the two datasets with the new veto list! 
```
python perModuleXSEC_mergeRaw.py -d 2018Ajobs/ --veto vetoBA.txt -l vetoAB
python perModuleXSEC_mergeRaw.py -d 2018Bjobs/ --veto vetoBA.txt -l vetoBA
```
Then proceed to run the comparison again to check your work
```
python compareTwoModXSECs.py --files output_vetoAB.pkl,output_vetoBA.pkl -b 1 -w 0.10 --labels AB1,BA1 --vetoList vetoBA.txt
```
then gather this lists to form a master list. 
