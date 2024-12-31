#Pythia fragment for filtered X(3872) -> J/psi(mu+mu-)gamma at 13.6TeV
#author: Jhovanny Andres Mejia
#email: jhovanny.andres.mejia.guisao@cern.ch

## this is a request to 5.02 TeV PbPb (Run2)
##https://github.com/boundino/HFAnaGenFrags/tree/master/Run2018PbPb502/X3872ana/python
## This is a request to 13.6 TeV (Run3)
##https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=X3872ToJPsi2Pi_JPsiTo2Mu_TuneCP5_13p6TeV_pythia8-evtgen&page=0&shown=127
## This is BPH-17-005 setup in BsToXPhi
##https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=BsToXPhi_MuTrkFilter_DGamma0_TuneCP5_13TeV-pythia8-evtgen&page=0&shown=127
## other examples
##https://github.com/cms-data/GeneratorInterface-EvtGenInterface/blob/master/incl_BtoX3872_Jpsipipi.dec
##https://github.com/cms-data/GeneratorInterface-EvtGenInterface/blob/master/Onia_mumu_withX3872.dec

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            #list_forced_decays = cms.vstring('MyX','MyX'),
            #operates_on_particles = cms.vint32(20443,20443),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# Particles updated from PDG2024 https://pdglive.lbl.gov/Viewer.action
# This is the decay file for X(3872)->Jpsi(mu+mu-)gamma
#
Particle   J/psi       3.0969000e+00   9.2600000e-05 ## 443
Particle   chi_c1      3.8716400e+00   0.00119 ## 20443 with X mass 

Alias      MyX(3872)   chi_c1
ChargeConj MyX(3872)   MyX(3872)
Alias      MyJ/psi     J/psi
ChargeConj MyJ/psi     MyJ/psi

Decay MyJ/psi
 1.0000  mu+     mu-          PHOTOS  VLL;
Enddecay

Decay MyX(3872)
1.000   Mypsi  gamma             PHSP;
Enddecay

End
"""
            ),
            operates_on_particles = cms.vint32(20443), 
            list_forced_decays = cms.vstring('MyX(3872)'),  
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring( # put below any needed pythia parameter
            '541:m0 = 6.27447', ## Bc mass
            '541:tau0 = 0.151995', ## Bc lifetime in c*tau/mm 
            '5122:m0 = 5.61960', ## Lb mass 
            '5122:tau0 = 0.439', ## Lb lifetime in c*tau/mm 299792458*1000* 0.964*1519*10^(-15)
            '5232:m0 = 5.7919', ## Xib0 mass 
            '5232:tau0 = 0.428', ## Xib0 lifetime in c*tau/mm 299792458*1000* 0.964*1480*10^(-15)
            '5132:m0 = 5.7970', ## Xib- mass 
            '5132:tau0 = 0.454', ## Xib- lifetime in c*tau/mm 299792458*1000* 0.964*1572*10^(-15)
            '5132:m0 = 6.0452', ## Omegab- mass 
            '5132:tau0 = 0.474', ## Omegab- lifetime in c*tau/mm 299792458*1000* 0.964*1640*10^(-15)
            '443:m0=3.0969',    ## Jpsi
            '20443:m0=3.87164', ## changing chi_c1 mass to match X(3872)
            '20443:mMin=3.86164', ## changing chi_c1 mass to match X(3872)
            '20443:mMax=3.88164', ## changing chi_c1 mass to match X(3872)
            '20443:mWidth=0.00119', ## changing chi_c1 with to match X(3872)
            'Charmonium:states(3PJ) = 20443,445',   # is it better to generating only Chi_c1 particle (20443)??
            'Charmonium:O(3PJ)[3P0(1)] = 0.05,0.05',
            'Charmonium:O(3PJ)[3S1(8)] = 0.0031,0.0031',
            'Charmonium:gg2ccbar(3PJ)[3PJ(1)]g = on,on',
            'Charmonium:qg2ccbar(3PJ)[3PJ(1)]q = on,on',
            'Charmonium:qqbar2ccbar(3PJ)[3PJ(1)]g = on,on',
            'Charmonium:gg2ccbar(3PJ)[3S1(8)]g = on,on',
            'Charmonium:qg2ccbar(3PJ)[3S1(8)]q = on,on',
            'Charmonium:qqbar2ccbar(3PJ)[3S1(8)]g = on,on',
            'PhaseSpace:pTHatMin = 5.', 
#           'PTFilter:filter = on', # this turn on the filter
#           'PTFilter:quarkToFilter = 4', # PDG id of q quark
#           'PTFilter:scaleToFilter = 2.0'),
#           'Charmonium:states(3P1) = 20443',
#
            #'ProcessLevel:all = off',
            #'ProcessLevel:resonanceDecays = on'
            #'HardQCD:gg2ccbar = on',
            #'HardQCD:qqbar2ccbar = on',
            #"SoftQCD:nonDiffractive = on",
            #'HardQCD:all = on',
#
                           ),
                           parameterSets = cms.vstring('pythia8CommonSettings',
                                                       'pythia8CP5Settings',
                                                       'processParameters'
                           )
                        )
)

#from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
#generator = ExternalGeneratorFilter(_generator)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

###### Filters ##########

xxfilter = cms.EDFilter("PythiaDauVFilter",
        NumberDaughters = cms.untracked.int32(2),
        ParticleID      = cms.untracked.int32(20443),  
        DaughterIDs     = cms.untracked.vint32(443, 22),
        MinPt           = cms.untracked.vdouble(6.0, 0.2), 
        MinEta          = cms.untracked.vdouble(-5.0, -9999.0), 
        MaxEta          = cms.untracked.vdouble( 5.0,  9999.0)
)

jmmfilter = cms.EDFilter("PythiaDauVFilter",
            NumberDaughters = cms.untracked.int32(2),
            MotherID        = cms.untracked.int32(20443),
            ParticleID      = cms.untracked.int32(443),
            DaughterIDs     = cms.untracked.vint32(13, -13),
            MinPt           = cms.untracked.vdouble(3.0, 3.0),
            MinEta          = cms.untracked.vdouble(-2.6, -2.6),
            MaxEta          = cms.untracked.vdouble( 2.6,  2.6)
        )

ProductionFilterSequence = cms.Sequence(generator*xxfilter*jmmfilter)
