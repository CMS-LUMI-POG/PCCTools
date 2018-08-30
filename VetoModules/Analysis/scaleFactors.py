#########################
#Author: Sam Higginbotham
'''

* File Name : scaleFactors.py

* Purpose :

* Creation Date : 30-08-2018

* Last Modified :

'''
#########################
import pickle
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("--files", help="Comma-separated list of file paths.")
parser.add_argument("--label", default="test", help="Comma-separated list of labels for two files")
parser.add_argument("-b","--batch", default=0, help="In batch mode?")
args=parser.parse_args()


if args.batch!=0:
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

filename1=args.files.split(",")[0]
filename2=args.files.split(",")[1]


file1=open(filename1)
file2=open(filename2)

dict1=pickle.load(file1)
dict2=pickle.load(file2)

mods1=dict1.keys()
mods2=dict2.keys()

dictSF={}
commonMods=list(set(mods1).intersection(mods2))
dictSF["total"]=0
fileSFout=open("scaleFactors"+args.label+".txt","wb")
sf=0.0

for mod in commonMods:
    print "dictionary 1 ",dict1[mod],"dictionary 2 ",dict2[mod]
    dictSF[mod]=dict1[mod]/dict2[mod]
    fileSFout.write(str(mod)+","+str(dict1[mod]/dict2[mod]))
    fileSFout.write("\n")

pickSFout=open("scaleFactors"+args.label+".pkl","wb")
pickle.dump(dictSF,pickSFout)
fileSFout.close()
pickSFout.close()

