#!/usr/bin/python2.6
#submit condor jobs for preselection
#https://github.com/jingyuluo/PCC_type2_scan
import sys, os
import shutil
import getpass
import glob
import ROOT
import subprocess
import numpy
import argparse

parser=argparse.ArgumentParser()
#parser.add_argument("-h", "--help", help="Display this message.")
parser.add_argument("-a", default="0.001,0.002,0.004", help="Parameter a min,max,step.  Default:  0.076,0.077,0.1")
parser.add_argument("-n", default="0.000,0.001,0.002", help=" nonlinearity in type I effect. Default: -0.0100, 0.0100, 0.0001")
parser.add_argument("-b", default="0.0003,0.0016,0.00001", help="Parameter b min,max,step.  Default:  0.0006,0.0009,0.00005")
parser.add_argument("-c", default="0.009,0.020,0.0005", help="Parameter c min,max,step.  Default:  0.012,0.02,0.005")
parser.add_argument('--norm', default=1, type=int, help="divide by this number for reduce computation time,just renormalize for the study")
parser.add_argument("-d", "--dir", default="JobDir", help="For output and jobs.  Default: JobDir")
parser.add_argument("-f", "--file", default="Run2016B-LumiPixels-PromptReco-v2_June17_4965_4980_Random_certtree.root", help="The input certtree file")
args=parser.parse_args()

a=args.a.split(",")
alist=numpy.arange(float(a[0]),float(a[1]),float(a[2]))

n=args.n.split(",")
nlist=numpy.arange(float(n[0]),float(n[1]),float(n[2]))

b=args.b.split(",")
blist=numpy.arange(float(b[0]),float(b[1]),float(b[2]))

c=args.c.split(",")
clist=numpy.arange(float(c[0]),float(c[1]),float(c[2]))

#set paths

current=os.getcwd()

bashjob="base.sh"
pathbashjob="{0}/{1}".format(current, bashjob)
pyscript="lumiInfo_DerivePCCCorrections.py"
pathpyscript="{0}/{1}".format(current, pyscript)
filename = args.file
root_file="{0}/".format(current)+filename

for ia in alist:
    for ni in nlist:
        for ib in blist:
            for ic in clist:
                label="a"+str(ia)+"_n"+str(ni)+"_b"+str(ib)+"_c"+str(ic)
                if not os.path.isdir(args.dir): os.mkdir(args.dir)
             
                folder=args.dir+"/"+label
                if not os.path.isdir(folder): os.mkdir(folder)
                print("Creating and Submitting Job {0}".format(folder))

                os.chdir(folder)
       
                condorfname="Scan_condor_{0}".format(label)
            
                fcondor=open(condorfname, "w")
                fcondor.write("Executable = {0}\n".format(pathbashjob)) 
                fcondor.write("Universe = vanilla\n")
                fcondor.write("should_transfer_files = YES\n")
                fcondor.write("Proxy_filename = x509up\n")
                fcondor.write('Proxy_path = /afs/cern.ch/user/s/shigginb/private/$(Proxy_filename)\n')
                fcondor.write("transfer_input_files = {0:s},{1:s}\n".format(pathpyscript,filename))
                fcondor.write("Output = {0}/{1}/run.out\n".format(current, folder))
                fcondor.write("Error  = {0}/{1}/run.err\n".format(current, folder))
                fcondor.write("Log    = {0}/{1}/run.log\n".format(current, folder))

                                                                                    # 1           2         3          4      5      6       7         8
                fcondor.write("Arguments = $(Proxy_path) {0} {1} {2} {3} {4} {5} {6} {7}\n".format(filename, str(ia), str(ni), str(ib), str(ic), label, pyscript,args.norm))
                fcondor.write('request_cpus = 4\n')
                fcondor.write('+JobFlavour  = "longlunch"\n')
                fcondor.write('+AccountingGroup = "group_u_CMS.CAF.COMM"\n')
                fcondor.write("Queue\n")
                fcondor.close()

                os.system("condor_submit Scan_condor_{0}".format(label))
                os.chdir(current)
                #break
            #break
        #break

