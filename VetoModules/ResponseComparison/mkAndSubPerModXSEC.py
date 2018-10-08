import sys,os
import subprocess
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("-p",  "--path",  help="EOS path to PCCNTuples... /store/user/..")
parser.add_argument("-d", "--jobdir", default="JobsDir", help="Output directory")
parser.add_argument("-s", "--sub",    default=False, help="Submit jobs")
parser.add_argument("-r", "--run",    default="", help="run to select")
parser.add_argument('-fl','--flist',type=argparse.FileType('r'), help='File List of PCC ntuples')
args=parser.parse_args()


def MakeJob(outputdir,filename,jobid):
    joblines=[]

    joblines.append("cd "+outputdir)
    joblines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh")
    joblines.append("cmsenv")
    joblines.append("echo 'starting script'")
    
    scriptCMD="python ../perModuleXSEC_2017format.py -f "+filename+" -l "+args.jobdir+"_"+str(jobid)
    if args.run!="":
        scriptCMD=scriptCMD+" -r "+args.run

    joblines.append(scriptCMD)

    scriptFile=open(outputdir+"/job_"+str(jobid)+".sh","w+")
    for line in joblines:
        scriptFile.write(line+"\n")
                        
    scriptFile.close()


def SubmitJob(job,queue="cmscaf1nd"):
    cmd="bsub -q "+queue+" -J "+args.jobdir+"_"+job+" -o "+args.jobdir+"_"+job+".log < "+str(job)
    output=os.system(cmd)
    if output!=0:
        print job,"did not submit properly"
        print cmd



if not os.path.exists(args.jobdir):
    os.makedirs(args.jobdir)

os.chdir(args.jobdir)
filelist=[]
#if args.path.find("/store")==0 and args.flist=="":
#    filenames=subprocess.check_output(["/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select","ls", args.path])
#    filenames=filenames.split("\n")
#    for filename in filenames:
#        if filename.find(".root")!=-1:
#            filelist.append("root://eoscms//eos/cms"+args.path+"/"+filename)
#else:
#    for filename in os.listdir(args.path):
#        filelist.append(args.path+"/"+filename)

if args.flist!="":
    try: 
        with args.flist as f: 
            print "opening list ",f
            lines = f.readlines()
            for line in lines:
                filelist.append(line.split('\n')[0])
    except:
        print "File Read Error!"

outputdir=os.getcwd()
print "Submitting",len(filelist),"jobs."
for filename in filelist:
    print filename
    jobid=filename.split("/")[-1]
    MakeJob(outputdir,filename,jobid)
    if args.sub:
        SubmitJob("job_"+jobid+".sh")

