#Pythia fragment for filtered Bu -> chicK -> J/psi(mu+mu-)gammaK at 13.6TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/ChiProduction/py8_BuChic1K_EvtGen_TuneCUETP8M1_13TeV_cfi.py

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *


_generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('MyB+','MyB-'),
            operates_on_particles = cms.vint32(521,-521),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for B -> Chi_c1(Jpsi ( -> mu mu ) gamma) K+
#
Alias      MyB+   B+
Alias      MyB-   B-
ChargeConj MyB-   MyB+

Alias MyJ/psi J/psi
ChargeConj MyJ/psi MyJ/psi

Alias Mychi_c1 chi_c1
ChargeConj Mychi_c1 Mychi_c1

Decay MyJ/psi
 1.0000  mu+        mu-                    PHOTOS VLL ;
Enddecay

Decay Mychi_c1
 1.0000  MyJ/psi    gamma                  VVP 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ;
Enddecay

Decay MyB+
# 0.0168  Mychi_c1   K+                   SVS ;
 1.0000  Mychi_c1   K+                   SVS ;

Enddecay
CDecay MyB-

End
"""
            ),
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('HardQCD:all = on',
                                        'PhaseSpace:pTHatMin = 8.',
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

###### Filters ##########
# Next two muon filter are derived from muon reconstruction

bufilter = cms.EDFilter("PythiaDauVFilter",
    ParticleID = cms.untracked.int32(521),
    MotherID = cms.untracked.int32(0),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(20443, 321),
    MinPt = cms.untracked.vdouble(0.0, 0.4),
    MaxEta = cms.untracked.vdouble(9999., 2.5),
    MinEta = cms.untracked.vdouble(-9999., -2.5)
)

chic1filter = cms.EDFilter("PythiaDauVFilter",
    ParticleID = cms.untracked.int32(20443),
    MotherID = cms.untracked.int32(521),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(443, 22),
    MinPt = cms.untracked.vdouble(7.0, 0.2),
    MaxEta = cms.untracked.vdouble(9999., 9999.),
    MinEta = cms.untracked.vdouble(-9999., -9999.)
)

muminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20443),
    MinPt = cms.untracked.vdouble(0.5, 0.5, 1.5, 1.5, 2.5),
    ParticleID = cms.untracked.int32(443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(1.6, -2.4, 1.2, -1.6, -1.2),
    MaxEta = cms.untracked.vdouble(2.4, -1.6, 1.6, -1.2, 1.2),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(-13, -13, -13, -13, -13)
)

muplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20443),
    MinPt = cms.untracked.vdouble(0.5, 0.5, 1.5, 1.5, 2.5),
    ParticleID = cms.untracked.int32(443),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(1.6, -2.4, 1.2, -1.6, -1.2),
    MaxEta = cms.untracked.vdouble(2.4, -1.6, 1.6, -1.2, 1.2),
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(13, 13, 13, 13, 13)
)

ProductionFilterSequence = cms.Sequence(generator*bufilter*chic1filter*muplusfilter*muminusfilter)
