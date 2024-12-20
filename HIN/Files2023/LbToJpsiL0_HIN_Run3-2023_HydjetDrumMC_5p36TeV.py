#Pythia fragment for filtered Lambdab -> J/psi(->mumu) Lambda(->Ppi) at 5.36TeV
#author: jhovanny.andres.mejia.guisao@cern.ch 

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
#from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import * ## This was in 2018 silmulation
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(5362.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyLambdab0','MyantiLambdab0'),
            operates_on_particles = cms.vint32(5122,-5122),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay Lambdab -> J/psi(->mumu) Lambda(->Ppi)
#
Alias      MyLambdab0       Lambda_b0
Alias      MyantiLambdab0   anti-Lambda_b0
ChargeConj MyLambdab0       MyantiLambdab0
Alias      MyLambda         Lambda0
Alias      MyLambdabar      anti-Lambda0
ChargeConj MyLambdabar      MyLambda
Alias      MyJpsi           J/psi
ChargeConj MyJpsi           MyJpsi
#
Decay MyLambdab0
1.000  MyLambda  MyJpsi  PHSP;
Enddecay
Decay MyantiLambdab0
1.000  MyLambdabar  MyJpsi  PHSP;
Enddecay
#
Decay MyJpsi
  1.000         mu+       mu-         PHOTOS VLL;
Enddecay
End
"""
            ),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            #'HardQCD:gg2bbbar    = on ',
            #'HardQCD:qqbar2bbbar = on ',
            #'HardQCD:hardbbbar   = on',
            'PhaseSpace:pTHatMin = 0.',
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

###### Filters ##########

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(5122),
    DaughterIDs     = cms.untracked.vint32(443, 3122),
    MinPt           = cms.untracked.vdouble(0.5, 0.1),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999., 9999.)
    )

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(5122),
    ParticleID      = cms.untracked.int32(443),
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(1.0, 1.0),
    MinEta          = cms.untracked.vdouble(-2.7, -2.7),
    MaxEta          = cms.untracked.vdouble( 2.7, 2.7)
    )

ProductionFilterSequence = cms.Sequence(generator*decayfilter*jpsifilter)
