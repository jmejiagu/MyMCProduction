#Pythia fragment for filtered Bc2S -> Bc(J/psi(mu+mu-)pi)pipi at 13.0TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/lhe-custom-hadronization/bcstar-pythia-had-evtgen-cuep8m1.py
# Als0 taken like Run2: https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=BcToJpsPi_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen&page=-1&shown=127

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(True),
                         comEnergy = cms.double(13000.),
                         ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                             decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
#                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bc_2014.pdl'),
                             particle_property_file = cms.FileInPath('evt_Bc_2014.pdl'),
                             convertPythiaCodes = cms.untracked.bool(False),
                             user_decay_embedded= cms.vstring(
"""
Particle B_c*+     6.34000 0.00000
Particle B_c+      6.27490 0.00000
Particle B_c(2S)+  6.87120 0.00000
Particle B_c*(2S)+ 6.90300 0.00000

Alias B_c+_SIGNAL B_c+
Alias B_c-_SIGNAL B_c-
Alias myJ/psi J/psi
ChargeConj myJ/psi myJ/psi
ChargeConj B_c+_SIGNAL B_c-_SIGNAL

Decay B_c(2S)+
  1.0 B_c+_SIGNAL pi+ pi-  PHSP;
Enddecay
CDecay B_c(2S)-

Decay B_c*(2S)+
  1.0 B_c*+       pi+ pi-  PHSP;
Enddecay
CDecay B_c*(2S)-

Decay B_c*+
  1.0 B_c+_SIGNAL  gamma   VSP_PWAVE;
Enddecay
CDecay B_c*-

Decay B_c+_SIGNAL
1.0   myJ/psi  pi+         SVS;
Enddecay
CDecay B_c-_SIGNAL

Decay myJ/psi
1.0   mu+  mu-             PHOTOS  VLL;
Enddecay

End
"""
                             ),
                             operates_on_particles = cms.vint32(100541,100543), 
                            # list_forced_decays = cms.vstring('MyBc+','MyBc-'),  
                           ),
                           parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           processParameters = cms.vstring( # put below any needed pythia parameter
#
            '100541:new = B_c(2S)+ B_c(2S)- 1 3 0 6.8712000e+00 0.0000000e+00 6.8712 6.8712 0.0000000e+00',
            '100541:isResonance = false',
            '100541:addChannel = 1 1.0 0 541 211 -211',
            '100541:mayDecay = off',
#
            '100543:new = B_c*(2S)+ B_c*(2S)- 3 3 0 6.9030000e+00 0.0000000e+00 6.903 6.903 0.0000000e+00',
            '100543:isResonance = false',
            '100543:addChannel = 1 1.0 0 543 211 -211',
            '100543:mayDecay = off',
#
            '543:m0 = 6.34000',
            '543:tau0 = 0.',
            '543:mayDecay = off',
#
            '541:m0 = 6.27447',
            '541:tau0 = 0.153',
            '541:mayDecay = off',
#
            'ProcessLevel:all = off',
            'ProcessLevel:resonanceDecays = on'
#
                           ),
                           parameterSets = cms.vstring('pythia8CommonSettings',
                                                       'pythia8CP5Settings',
                                                       'processParameters'
                           )
                        )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bc2sgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-211, 211),
    MaxEta = cms.untracked.vdouble(999., 999.),
    MinEta = cms.untracked.vdouble(-999., -999.),
    MinPt = cms.untracked.vdouble(0., 0.),
    NumberDaughters = cms.untracked.int32(2),
#    ParticleID = cms.untracked.int32(100543),
    ParticleID = cms.untracked.int32(100541),                         
    verbose = cms.untracked.int32(0)
)

bcgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(211),
    MaxEta = cms.untracked.vdouble(2.6),
    MinEta = cms.untracked.vdouble(-2.6),
    MinPt = cms.untracked.vdouble(0.9),
    NumberDaughters = cms.untracked.int32(1),
    ParticleID = cms.untracked.int32(541),
    verbose = cms.untracked.int32(0)
)

jpsifilter = cms.EDFilter("PythiaDauVFilter",
  verbose         = cms.untracked.int32(0),
  NumberDaughters = cms.untracked.int32(2),
  MotherID        = cms.untracked.int32(541),
  ParticleID      = cms.untracked.int32(443),
  DaughterIDs     = cms.untracked.vint32(13, -13),
  MinPt           = cms.untracked.vdouble(2.6, 2.6),
  MinEta          = cms.untracked.vdouble(-2.6, -2.6),
  MaxEta          = cms.untracked.vdouble( 2.6,  2.6)
)

ProductionFilterSequence = cms.Sequence(generator*bc2sgenfilter*bcgenfilter*jpsifilter)
