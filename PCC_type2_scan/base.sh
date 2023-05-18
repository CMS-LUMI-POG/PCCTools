#! /bin/bash
cd ${_CONDOR_SCRATCH_DIR}
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
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
python3 $8 -l $7 -i $2 -p "$3,$4,$5,$6" --norm $9 --noType1
cp  Overall_*root ${_CONDOR_SCRATCH_DIR}/.
cp  *png ${_CONDOR_SCRATCH_DIR}/.
