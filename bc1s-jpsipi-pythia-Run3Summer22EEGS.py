#Pythia fragment for filtered Bc -> J/psi(mu+mu-)pi at 13.6TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/lhe-custom-hadronization/bc1s-jpsipi-pythia-had-evtgen-cp5.py

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(True),
                         comEnergy = cms.double(13600.),
                         ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                             decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bc_2014.pdl'),
                             convertPythiaCodes = cms.untracked.bool(False),
                             user_decay_embedded= cms.vstring(
"""
Particle B_c+      6.27490 0.00000

Alias B_c+_SIGNAL B_c+
Alias B_c-_SIGNAL B_c-
Alias myJ/psi J/psi
ChargeConj myJ/psi myJ/psi
ChargeConj B_c+_SIGNAL B_c-_SIGNAL

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
                             operates_on_particles = cms.vint32(541), 
                             list_forced_decays = cms.vstring('B_c+_SIGNAL','B_c-_SIGNAL'),  
                           ),
                           parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           processParameters = cms.vstring( # put below any needed pythia parameter
#
            '541:m0 = 6.2749',
            '541:tau0 = 0.151995',
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

bcgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(211),
    MaxEta = cms.untracked.vdouble(2.5),
    MinEta = cms.untracked.vdouble(-2.5),
    MinPt = cms.untracked.vdouble(1.0),
    NumberDaughters = cms.untracked.int32(1),
    ParticleID = cms.untracked.int32(541),
    verbose = cms.untracked.int32(0)
)

mumugenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MinPt = cms.untracked.vdouble(3.5, 3.5),
    MotherID = cms.untracked.int32(541),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(443),
    verbose = cms.untracked.int32(0)
)

ProductionFilterSequence = cms.Sequence(generator*bcgenfilter*mumugenfilter)
