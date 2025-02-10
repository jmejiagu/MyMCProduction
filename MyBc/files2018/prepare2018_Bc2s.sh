#!/bin/bash

#all steps from https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=XibToJpsiLambdaK_JMM_MMFilter_DGamma0_TuneCP5_13TeV-pythia8-evtgen&page=-1&shown=127

# step0 GEN
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_30_patch1/src ] ; then
  echo release CMSSW_10_6_30_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_30_patch1
fi
cd CMSSW_10_6_30_patch1/src
eval `scram runtime -sh`

# Configuration parameters
CHANNEL_DECAY="1-BcToJpsipi"
step0_fragmentfile="bc1s-jpsipi-pythia-Run2Summer20UL_2018.py"
step00_configfile="step00-GEM-${CHANNEL_DECAY}-run_cfg.py"
step00_resultfile="step00-GEM-${CHANNEL_DECAY}-result.root"
step0_configfile="step0-GEM-${CHANNEL_DECAY}-run_cfg.py"
step0_resultfile="step0-GEM-${CHANNEL_DECAY}-result.root"

# Download fragment from myGitHub
curl -s -k https://raw.githubusercontent.com/jmejiagu/MyMCProduction/main/files2018/$step0_fragmentfile --retry 3 --create-dirs -o Configuration/GenProduction/python/$step0_fragmentfile
[ -s Configuration/GenProduction/python/$step0_fragmentfile ] || exit $?;

scram b
cd ../..

##EVENTS=10000

# cmsDriver "00" command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18GEN-00209
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18pLHEGEN-00087
cmsDriver.py Configuration/GenProduction/python/$step0_fragmentfile --python_filename $step00_configfile --eventcontent LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier LHE --fileout file:$step00_resultfile --conditions 106X_upgrade2018_realistic_v4  --step NONE --filein file:bcvegpy.lhe --era Run2_2018 --no_exec --mc -n -1

# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/$step0_fragmentfile --python_filename $step0_configfile --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --fileout file:$step0_resultfile --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --filein file:$step00_resultfile --era Run2_2018 --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper \nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step0_configfile
echo cmsDriver for step-0 Gen ok

# step1 SIM
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

#mv ../../Configuration .
scram b
cd ../..

# Configuration parameters
step1_configfile="step1-SIM-${CHANNEL_DECAY}-run_cfg.py"
step1_resultfile="step1-SIM-${CHANNEL_DECAY}-result.root"

# cmsDriver command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18SIM-00332
cmsDriver.py  --python_filename $step1_configfile --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:$step1_resultfile --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:$step0_resultfile --era Run2_2018 --runUnscheduled --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step1_configfile
echo cmsDriver for step-1 SIM ok


# step2 DIGIPremix
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

#mv ../../Configuration .
scram b
cd ../..

# Configuration parameters
step2_configfile="step2-DIGIPremix-${CHANNEL_DECAY}-run_cfg.py"
step2_resultfile="step2-DIGIPremix-${CHANNEL_DECAY}-result.root"

# cmsDriver command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18DIGIPremix-00287
cmsDriver.py  --python_filename $step2_configfile --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:$step2_resultfile --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:$step1_resultfile --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n -1
sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step2_configfile
echo cmsDriver for step-2 DIGIPremix ok

# step3 HLT
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_16_UL/src ] ; then
  echo release CMSSW_10_2_16_UL already exists
else
  scram p CMSSW CMSSW_10_2_16_UL
fi
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`

#mv ../../Configuration .
scram b
cd ../..

# Configuration parameters
step3_configfile="step3-HLT-${CHANNEL_DECAY}-run_cfg.py"
step3_resultfile="step3-HLT-${CHANNEL_DECAY}-result.root"

# cmsDriver command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18HLT-00332
cmsDriver.py  --python_filename $step3_configfile --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:$step3_resultfile --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --geometry DB:Extended --filein file:$step2_resultfile --era Run2_2018 --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step3_configfile
echo cmsDriver for step-3 HLT ok

# step4 RECO
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

#mv ../../Configuration .
scram b
cd ../..

# Configuration parameters
step4_configfile="step4-RECO-${CHANNEL_DECAY}-run_cfg.py"
step4_resultfile="step4-RECO-${CHANNEL_DECAY}-result.root"

# cmsDriver command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18RECO-00332
cmsDriver.py  --python_filename $step4_configfile --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:$step4_resultfile --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:$step3_resultfile --era Run2_2018 --runUnscheduled --no_exec --mc -n -1

sed -i "20 a from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper\nrandSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)\nrandSvc.populate()" $step4_configfile
echo cmsDriver for step-4 RECO ok

# step4 MiniAOD
export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_20/src ] ; then
  echo release CMSSW_10_6_20 already exists
else
  scram p CMSSW CMSSW_10_6_20
fi
cd CMSSW_10_6_20/src
eval `scram runtime -sh`

##mv ../../Configuration .
scram b
cd ../..

# Configuration parameters
step5_configfile="step5-MINIAODSIM-${CHANNEL_DECAY}-run_cfg.py"
step5_resultfile="step5-MINIAODSIM-${CHANNEL_DECAY}-result.root"

# cmsDriver command
#cmsdriver origin: https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_setup/BPH-RunIISummer20UL18MiniAODv2-00329
cmsDriver.py  --python_filename $step5_configfile --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:$step5_resultfile --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:$step4_resultfile --era Run2_2018 --runUnscheduled --no_exec --mc -n -1

echo cmsDriver for step-5 MINIAODSIM ok
