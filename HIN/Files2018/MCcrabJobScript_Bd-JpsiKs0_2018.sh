#!/bin/bash

CHANNEL_DECAY="1-BdtoJpsiKs0"
YEAR="2018"

GEN_REL="CMSSW_10_3_2"
GEN_SCRAM="slc6_amd64_gcc700"
RECO_REL="CMSSW_10_3_3_patch1"
RECO_SCRAM="slc6_amd64_gcc700"
MINI_REL="CMSSW_11_2_2"
MINI_SCRAM="slc7_amd64_gcc900"

echo "================= cmssw environment prepration Gen step ===================="
source /cvmfs/cms.cern.ch/cmsset_default.sh
#export SCRAM_ARCH=$GEN_SCRAM
if [ -r $GEN_REL/src ] ; then
  echo release $GEN_REL already exists
else
  scram p CMSSW $GEN_REL
fi
cd $GEN_REL/src
eval `scram runtime -sh`
scram b
cd ../../

echo "================= PB: CMSRUN starting Gen step ===================="
# PSet is the name that crab assigns to the config file of the job
cmsRun -j ${CHANNEL_DECAY}_step0.log  -p PSet.py
#cmsRun -j ${CHANNEL_DECAY}_step0.log -p step0-RAWSIM-1-BdtoJpsiKs0-run_cfg.py


echo "================= cmssw environment prepration Reco step ===================="
#export SCRAM_ARCH=$RECO_SCRAM
if [ -r $RECO_REL/src ] ; then
  echo release $RECO_REL already exists
else
  scram p CMSSW $RECO_REL
fi
cd $RECO_REL/src
eval `scram runtime -sh`
scram b
cd ../../

echo "================= PB: CMSRUN starting Reco step1 ===================="
#cmsRun -e -j ${CHANNEL_DECAY}_step1.log step1-PREMIXRAW-1-BdtoJpsiKs0-run_cfg.py
cmsRun -e -j ${CHANNEL_DECAY}_step1.log step1-PREMIXRAW-${CHANNEL_DECAY}-run_cfg.py
#cleaning
#rm -rfv step1-PREMIXRAW-${CHANNEL_DECAY}--result.root

echo "================= PB: CMSRUN starting Reco step2 ===================="
#cmsRun -e -j ${CHANNEL_DECAY}_step2.log  step2-AODSIM-1-BdtoJpsiKs0-run_cfg.py
cmsRun -e -j ${CHANNEL_DECAY}_step2.log step2-AODSIM-${CHANNEL_DECAY}-run_cfg.py


echo "================= cmssw environment prepration MiniAOD step ===================="
#export SCRAM_ARCH=$MINI_SCRAM
if [ -r $MINI_REL/src ] ; then
  echo release $MINI_REL already exists
else
  scram p CMSSW $MINI_REL
fi
cd $MINI_REL/src
eval `scram runtime -sh`
scram b
cd ../../

echo "================= PB: CMSRUN starting MiniAOD step ===================="
#cmsRun -e -j ${CHANNEL_DECAY}_step3.log  step3-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py
#cmsRun -e -j FrameworkJobReport.xml  step3-MINIAODSIM-1-BdtoJpsiKs0-run_cfg.py
cmsRun -e -j FrameworkJobReport.xml  step3-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py
