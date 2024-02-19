#!/bin/bash

#all steps from https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=BdToJpsiK0s_Unbiased_TuneCP5_13p6TeV_pythia8-evtgen&page=0&shown=2151940099

export SCRAM_ARCH=el8_amd64_gcc10

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_14_patch3/src ] ; then
  echo release CMSSW_12_4_14_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_14_patch3
fi
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

# Configuration parameters
CHANNEL_DECAY="1-BuToChicK"
step0_fragmentfile="bu-chicK-jpsigammaK-pythia-Run3Summer22EEGS.py"
step0_configfile="step0-RAWSIM-${CHANNEL_DECAY}-run_cfg.py"
step0_resultfile="step0-RAWSIM-${CHANNEL_DECAY}-result.root"

# Download fragment from myGitHub
curl -s -k https://raw.githubusercontent.com/jmejiagu/MyMCProduction/main/$step0_fragmentfile --retry 3 --create-dirs -o Configuration/GenProduction/python/$step0_fragmentfile
[ -s Configuration/GenProduction/python/$step0_fragmentfile ] || exit $?;

scram b
cd ../..

EVENTS=500

#cmsDriver.py Configuration/GenProduction/python/$step0_fragmentfile --python_filename $step0_configfile --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:$step0_resultfile --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n $EVENTS || exit $? ;

# cmsDriver command origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-Run3Summer22EEGS-00112
cmsDriver.py Configuration/GenProduction/python/$step0_fragmentfile \
	     --fileout file:$step0_resultfile --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring \
	     --datatier GEN-SIM --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM \
	     --geometry DB:Extended --era Run3 --python_filename $step0_configfile --no_exec -n $EVENTS || exit $? ;


sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper \nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step0_configfile
echo cmsDriver for step-0 Gen ok


# step1 DIGI, 

export SCRAM_ARCH=el8_amd64_gcc10
#for some reason this doesn't work

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_14_patch3/src ] ; then
  echo release CMSSW_12_4_14_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_14_patch3
fi
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

scram b
cd ../..

# Configuration parameters
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_test/BPH-Run3Summer22EEDRPremix-00130
step1_configfile="step1-PREMIXRAW-${CHANNEL_DECAY}-run_cfg.py"
step1_resultfile="step1-PREMIXRAW-${CHANNEL_DECAY}-result.root"

cmsDriver.py  --python_filename $step1_configfile --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring \
	      --datatier GEN-SIM-RAW --fileout file:$step1_resultfile --pileup_input "dbs:/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX" \
	      --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v14 --procModifiers premix_stage2,siPixelQualityRawToDigi \
	      --geometry DB:Extended --filein file:$step0_resultfile --datamix PreMix --era Run3 --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step1_configfile
echo cmsDriver for step-1 DIGI ok


# step2 

export SCRAM_ARCH=el8_amd64_gcc10
#for some reason this doesn't work

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_14_patch3/src ] ; then
  echo release CMSSW_12_4_14_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_14_patch3
fi
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

scram b
cd ../..


# Configuration parameters
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_test/BPH-Run3Summer22EEDRPremix-00130
step2_configfile="step2-AODSIM-${CHANNEL_DECAY}-run_cfg.py"
step2_resultfile="step2-AODSIM-${CHANNEL_DECAY}-result.root"

cmsDriver.py  --python_filename $step2_configfile --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:$step2_resultfile --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM --procModifiers siPixelQualityRawToDigi --geometry DB:Extended --filein file:$step1_resultfile --era Run3 --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step2_configfile
echo cmsDriver for step-2 RECO ok


# step3 MINIAODSIM
#for some reason this doesn't work

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_14_patch3/src ] ; then
  echo release CMSSW_12_4_14_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_14_patch3
fi
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

scram b
cd ../..

# Configuration parameters 
step3_configfile="step3-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py"
step3_resultfile="step3-MINIAODSIM-${CHANNEL_DECAY}-result.root"

#cmsDriver command origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_test/BPH-Run3Summer22EEMiniAODv3-00130
cmsDriver.py  --python_filename $step3_configfile --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:$step3_resultfile --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step PAT --geometry DB:Extended --filein file:$step2_resultfile --era Run3 --no_exec --mc -n -1

echo cmsDriver for step-3 MINIAOD ok 







