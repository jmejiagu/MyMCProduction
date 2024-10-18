#!/bin/bash

## for 2018 all steps from https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=BtoPsi2S_pThat-2_TuneCP5-EvtGen_HydjetDrumMB_5p02TeV_pythia8&page=0&shown=127
## for 2023 I have follow the suggestions by Saray and the oficial twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MCFor2023PbPb5p36TeV

#export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_13_0_20_HeavyIon/src ] ; then
  echo release CMSSW_13_0_20_HeavyIon already exists
else
  scram p CMSSW CMSSW_13_0_20_HeavyIon
fi
cd CMSSW_13_0_20_HeavyIon/src
eval `scram runtime -sh`

# Configuration parameters
CHANNEL_DECAY="1-LbtoJpsiL0"
step0_fragmentfile="LbToJpsiL0_HIN_Run3-2023_HydjetDrumMC_5p36TeV.py"
step0_configfile="step0-RAWSIM-${CHANNEL_DECAY}-run_cfg.py"
step0_resultfile="step0-RAWSIM-${CHANNEL_DECAY}-result.root"

## Download fragment from myGitHub
curl -s -k https://raw.githubusercontent.com/jmejiagu/MyMCProduction/refs/heads/main/HIN/Files2023/$step0_fragmentfile --retry 3 --create-dirs -o Configuration/GenProduction/python/$step0_fragmentfile
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

## Step 0, GSMix campaign (PYTHIA8 only)
## cmsdriver comman
cmsDriver.py  Configuration/GenProduction/python/$step0_fragmentfile --python_filename $step0_configfile --mc --eventcontent RAWSIM --datatier GEN-SIM --fileout file:$step0_resultfile --conditions 130X_mcRun3_2023_realistic_HI_v18 --beamspot MatchHI --step GEN,SIM --scenario HeavyIons --geometry DB:Extended --era Run3_pp_on_PbPb --pileup HiMixGEN --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM" --no_exec -n $EVENTS || exit $? ;     
### --customise Configuration/DataProcessing/Utils.addMonitoring, is this missing????

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper \nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step0_configfile
echo cmsDriver for step-0 Gen ok


## cmssw release for steps 1, 2, and 3
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_13_2_10/src ] ; then
  echo release CMSSW_13_2_10 already exists
else
  scram p CMSSW CMSSW_13_2_10
fi
cd CMSSW_13_2_10/src
eval `scram runtime -sh`

scram b
cd ../..

## Step 1, Digi campaign (DIGI-RAW)
## Configuration parameters
step1_configfile="step1-PREMIXRAW-${CHANNEL_DECAY}-run_cfg.py"
step1_resultfile="step1-PREMIXRAW-${CHANNEL_DECAY}-result.root"

## cmsDriver comman
cmsDriver.py --python_filename $step1_configfile --mc --eventcontent RAWSIM --datatier GEN-SIM-DIGI-RAW --conditions 132X_mcRun3_2023_realistic_HI_v9 --step DIGI:pdigi_hi_nogen,L1,DIGI2RAW,HLT:HIon --geometry DB:Extended --era Run3_pp_on_PbPb_2023 --filein file:$step0_resultfile --fileout file:$step1_resultfile  --pileup HiMix --pileup_input "dbs:/MinBias_Drum5F_5p36TeV_hydjet/HINPbPbSpring23GS-130X_mcRun3_2023_realistic_HI_v18-v2/GEN-SIM" --no_exec -n -1 ;  

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step1_configfile
echo cmsDriver for step-1 DIGI ok

## Step 2, Reco campaign (RECO)
## Configuration parameters 
step2_configfile="step2-AODSIM-${CHANNEL_DECAY}-run_cfg.py"
step2_resultfile="step2-AODSIM-${CHANNEL_DECAY}-result.root"

## cmsDriver comman
cmsDriver.py --python_filename $step2_configfile --mc --eventcontent AODSIM --datatier AODSIM --conditions 132X_mcRun3_2023_realistic_HI_v9 --customise_commands "process.hltSiStripRawToDigi.ProductLabel='rawDataCollector';process.hltScalersRawToDigi.scalersInputTag='rawDataCollector'" --step REPACK:DigiToApproxClusterRaw,RAW2DIGI,L1Reco,RECO --era Run3_pp_on_PbPb_approxSiStripClusters_2023 --filein file:$step1_resultfile --fileout file:$step2_resultfile --no_exec -n -1 ;
## --runUnscheduled,  is this missing????

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step2_configfile
echo cmsDriver for step-2 RECO ok


## step3, MINIAOD campaign
## Configuration parameters 
step3_configfile="step3-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py"
step3_resultfile="step3-MINIAODSIM-${CHANNEL_DECAY}-result.root"

## cmsDriver command
cmsDriver.py --python_filename $step3_configfile --mc --eventcontent MINIAODSIM --datatier MINIAODSIM --conditions 132X_mcRun3_2023_realistic_HI_v9 --step PAT --geometry DB:Extended --era Run3_pp_on_PbPb_2023 --filein file:$step2_resultfile --fileout file:$step3_resultfile --no_exec -n -1 ;
## runUnscheduled,  is this missing????
## --customise Configuration/DataProcessing/Utils.addMonitoring,  is this missing????      

echo cmsDriver for step-3 MINIAOD ok







