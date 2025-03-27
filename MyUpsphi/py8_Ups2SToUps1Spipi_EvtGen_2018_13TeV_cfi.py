# cfi file for Upsilon(2S) -> Upsilon(1S)pipi. Masses and widths are matched between pythia, evtgen and PDG 2024
#Pythia fragment for filtered Upsilon(2S) -> Upsilon(1S)pipi at 13.0TeV
#author: Jhovanny Andres Mejia
#email: jhovanny.andres.mejia.guisao@cern.ch

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('myUps2S'),    
            operates_on_particles = cms.vint32(100553),          # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Particle Upsilon(2S)  10.023400   0.00003198
Particle Upsilon      9.460400    0.00005402

Alias myUps2S Upsilon(2S)
Alias myUps   Upsilon

Decay myUps
1.0   mu+  mu-          PHOTOS  VLL;
Enddecay

Decay myUps2S
1.0   myUps pi+ pi-  PHSP;
Enddecay

End
"""
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3S1) = 100553',
            'Bottomonium:O(3S1)[3S1(1)] = 4.63',
            'Bottomonium:O(3S1)[3S1(8)] = 0.045',
            'Bottomonium:O(3S1)[1S0(8)] = 0.06',
            'Bottomonium:O(3S1)[3P0(8)] = 0.06',
            'Bottomonium:gg2bbbar(3S1)[3S1(1)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3S1(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[3S1(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[3S1(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[1S0(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[1S0(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[1S0(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3PJ(8)]g = on',
            'Bottomonium:qg2bbbar(3S1)[3PJ(8)]q = on',
            'Bottomonium:qqbar2bbbar(3S1)[3PJ(8)]g = on',
            'Bottomonium:gg2bbbar(3S1)[3S1(1)]gm = on',
#            
            'PhaseSpace:pTHatMin = 2.',
#            
            '100553:m0 = 10.023400',
            '100553:mWidth = 0.00003198',            
            '100553:mayDecay = off',       ## Pythia generates the particle but does not decay it, EvtGen will take care of that.
#            
            '553:m0 = 9.460400',
            '553:mWidth = 0.00005402',            
            '553:mayDecay = off',            
#            
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

# We will filter, first on the ID, then in the mass.

pwaveIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(100553),
    MinPt = cms.untracked.vdouble(0.0),
    MinEta = cms.untracked.vdouble(-9.0),
    MaxEta = cms.untracked.vdouble(9.0),
    Status = cms.untracked.vint32(2)
)

upsIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(553),
    MinPt = cms.untracked.vdouble(9.0),
    MinEta = cms.untracked.vdouble(-1.6),
    MaxEta = cms.untracked.vdouble(1.6),
    Status = cms.untracked.vint32(2)
)

# Next two muon filter are derived from muon reconstruction

muminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(100553),
    ParticleID = cms.untracked.int32(553),
    NumberDaughters = cms.untracked.int32(1),                             
    DaughterIDs = cms.untracked.vint32(-13),
    MinPt = cms.untracked.vdouble(3.0),                             
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
    
)

muplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(100553),
    ParticleID = cms.untracked.int32(553),
    NumberDaughters = cms.untracked.int32(1),                            
    DaughterIDs = cms.untracked.vint32(13),                            
    MinPt = cms.untracked.vdouble(3.0),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

#  two pion filter

piminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    ParticleID = cms.untracked.int32(100553),
    NumberDaughters = cms.untracked.int32(1),                             
    DaughterIDs = cms.untracked.vint32(-211),                             
    MinPt = cms.untracked.vdouble(0.5),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

piplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    ParticleID = cms.untracked.int32(100553),                            
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(211),                        
    MinPt = cms.untracked.vdouble(0.5),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

ProductionFilterSequence = cms.Sequence(generator*pwaveIDfilter*upsIDfilter*piminusfilter*piplusfilter*muminusfilter*muplusfilter)
