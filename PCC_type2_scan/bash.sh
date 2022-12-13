#! /bin/bash
cd ${_CONDOR_SCRATCH_DIR}
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700
export EOS_MGM_URL=root://eosuser.cern.ch
eval `scramv1 project CMSSW CMSSW_12_1_0_pre3`
cd CMSSW_12_1_0_pre3/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}/CMSSW_12_1_0_pre3/src/
cp ${_CONDOR_SCRATCH_DIR}/* .
scram b -j 4
eval `scramv1 runtime -sh`
ls -altrh

echo "Setup cmssw environment, running script now"

#python3 lumiInfo_DerivePCCCorrections_noKey.py
python3 $7 -l $6 -i $1 -r $8 -p "'$2,$3'" 
