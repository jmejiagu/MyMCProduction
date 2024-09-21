from CRABClient.UserUtilities import config
import datetime
import time

config = config()

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M')

channel = '1--BdtoJpsiKs0'
year = '2018'
step = 'PrivateMC-'+year
nEvents = 10000
NJOBS = 100
myrun = 'step0-RAWSIM-1-BdtoJpsiKs0-run_cfg.py'
myname = step+'-'+channel

config.General.requestName = step+'-'+channel+'-'+st
config.General.transferOutputs = True
config.General.transferLogs = False
config.General.workArea = 'crab_'+step+'-'+channel

config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = myrun
config.JobType.inputFiles = ['step1-PREMIXRAW-1-BdtoJpsiKs0-run_cfg.py',
                             'step2-AODSIM-1-BdtoJpsiKs0-run_cfg.py',
                             'step3-MINIAODSIM-1-BdtoJpsiKs0-run_cfg.py']
config.JobType.disableAutomaticOutputCollection = True
config.JobType.eventsPerLumi = 10000
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 3300
config.JobType.scriptExe = 'MCcrabJobScript_Bd-JpsiKs0_2018.sh'

#config.JobType.scriptArgs = ['CHANNEL_DECAY='+channel,'YEAR='+year] ## for MCcrabJobScript.sh if necessary
#config.JobType.outputFiles = ['MC-'+year+'-'+channel+'.root']
config.JobType.outputFiles = ['step3-MINIAODSIM-1-BdtoJpsiKs0-result.root']

config.Data.outputPrimaryDataset = myname
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = nEvents
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
#config.Data.outLFNDirBase = '/store/user/jmejiagu/'
config.Data.publication = False

config.Site.storageSite = 'T3_CH_CERNBOX'
#config.Site.storageSite = 'T2_CH_CERN'
#config.Site.storageSite = 'T2_IT_Bari'
