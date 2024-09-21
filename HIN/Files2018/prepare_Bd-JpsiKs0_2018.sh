#!/bin/bash

#all steps from https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=BtoPsi2S_pThat-2_TuneCP5-EvtGen_HydjetDrumMB_5p02TeV_pythia8&page=0&shown=127


export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_3_2/src ] ; then
  echo release CMSSW_10_3_2 already exists
else
  scram p CMSSW CMSSW_10_3_2
fi
cd CMSSW_10_3_2/src
eval `scram runtime -sh`

# Configuration parameters
CHANNEL_DECAY="1-BdtoJpsiKs0"
step0_fragmentfile="BdToJpsiKs0_HIN_Run2_HydjetDrumMC_5p02TeV.py"
step0_configfile="step0-RAWSIM-${CHANNEL_DECAY}-run_cfg.py"
step0_resultfile="step0-RAWSIM-${CHANNEL_DECAY}-result.root"

# Download fragment from myGitHub
curl -s -k https://raw.githubusercontent.com/jmejiagu/MyMCProduction/refs/heads/main/HIN/Files2018/$step0_fragmentfile --retry 3 --create-dirs -o Configuration/GenProduction/python/$step0_fragmentfile
[ -s Configuration/GenProduction/python/$step0_fragmentfile ] || exit $?;

scram b
cd ../..

# Maximum validation duration: 57600s
# Margin for validation duration: 30%
# Validation duration with margin: 57600 * (1 - 0.30) = 40320s
# Time per event for each sequence: 1.1030s
# Threads for each sequence: 1
# Time per event for single thread for each sequence: 1 * 1.1030s = 1.1030s
# Which adds up to 1.1030s per event
# Single core events that fit in validation duration: 40320s / 1.1030s = 36554
# Produced events limit in McM is 10000
# According to 0.0140 efficiency, validation should run 10000 / 0.0140 = 712758 events to reach the limit of 10000
# Take the minimum of 36554 and 712758, but more than 0 -> 36554
# It is estimated that this validation will produce: 36554 * 0.0140 = 512 events
EVENTS=1000

#Step 0
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/HIN-HINPbPbAutumn18GSHIMix-00005
cmsDriver.py Configuration/GenProduction/python/$step0_fragmentfile --python_filename $step0_configfile --eventcontent RAWSIM --pileup HiMixGEN --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:$step0_resultfile --pileup_input "dbs:/MinBias_Hydjet_Drum5F_2018_5p02TeV/HINPbPbAutumn18GS-103X_upgrade2018_realistic_HI_v11-v1/GEN-SIM" --conditions 103X_upgrade2018_realistic_HI_v11 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run2_2018_pp_on_AA --no_exec --mc -n $EVENTS || exit $? ;

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper \nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step0_configfile
echo cmsDriver for step-0 Gen ok


# step1 and  step2 GEN-SIM-RAW and AOD
export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_3_3_patch1/src ] ; then
  echo release CMSSW_10_3_3_patch1 already exists
else
  scram p CMSSW CMSSW_10_3_3_patch1
fi
cd CMSSW_10_3_3_patch1/src
eval `scram runtime -sh`

scram b
cd ../..

# Configuration parameters
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/HIN-HINPbPbAutumn18DR-00045
step1_configfile="step1-PREMIXRAW-${CHANNEL_DECAY}-run_cfg.py"
step1_resultfile="step1-PREMIXRAW-${CHANNEL_DECAY}-result.root"

step2_configfile="step2-AODSIM-${CHANNEL_DECAY}-run_cfg.py"
step2_resultfile="step2-AODSIM-${CHANNEL_DECAY}-result.root"

#cmsDriver comman
cmsDriver.py  --python_filename $step1_configfile --eventcontent RAWSIM --pileup HiMix --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:$step1_resultfile --pileup_input "dbs:/MinBias_Hydjet_Drum5F_2018_5p02TeV/HINPbPbAutumn18GS-103X_upgrade2018_realistic_HI_v11-v1/GEN-SIM" --conditions 103X_upgrade2018_realistic_HI_v11 --step DIGI:pdigi_hi_nogen,L1,DIGI2RAW,HLT:HIon --geometry DB:Extended --filein file:$step0_resultfile --era Run2_2018_pp_on_AA --no_exec --mc -n -1 ;

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step1_configfile
echo cmsDriver for step-1 DIGI ok

#cmsDriver comman
cmsDriver.py  --python_filename $step2_configfile --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:$step2_resultfile --conditions 103X_upgrade2018_realistic_HI_v11 --step RAW2DIGI,L1Reco,RECO --filein file:$step1_resultfile --era Run2_2018_pp_on_AA --runUnscheduled --no_exec --mc -n -1 ;

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step2_configfile
echo cmsDriver for step-2 RECO ok


# step3 MINIAODSIM
export SCRAM_ARCH=slc7_amd64_gcc900

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_11_2_2/src ] ; then
  echo release CMSSW_11_2_2 already exists
else
  scram p CMSSW CMSSW_11_2_2
fi
cd CMSSW_11_2_2/src
eval `scram runtime -sh`

scram b
cd ../..

# Configuration parameters 
step3_configfile="step3-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py"
step3_resultfile="step3-MINIAODSIM-${CHANNEL_DECAY}-result.root"

# cmsDriver command origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/HIN-HINPbPbSpring21MiniAOD-00181
cmsDriver.py  --python_filename $step3_configfile --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:$step3_resultfile --conditions 112X_upgrade2018_realistic_HI_v9 --step PAT --procModifiers run2_miniAOD_pp_on_AA_103X --geometry DB:Extended --filein file:$step2_resultfile --era Run2_2018_pp_on_AA runUnscheduled --no_exec --mc -n -1 ;

echo cmsDriver for step-3 MINIAOD ok 







