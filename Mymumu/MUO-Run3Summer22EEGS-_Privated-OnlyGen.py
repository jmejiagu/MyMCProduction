import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from  Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


generator = cms.EDFilter("Pythia8ConcurrentGeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(0.005074),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         crossSection = cms.untracked.double(171500000.0),
                         comEnergy = cms.double(13600.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'Charmonium:all = on',                       # Quarkonia, MSEL=61, including feed-down as well
            '443:onMode = off',                          # Turn off J/psi decays
            '443:onIfMatch = 13 -13',                    # just let J/psi -> mu+ mu-
            'PhaseSpace:pTHatMin = 2.'                   # be aware of this ckin(3) equivalent
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    )
        )
)

# Next two muon filter are derived from muon reconstruction
mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    MinP = cms.untracked.vdouble(0.0, 0.0),
    MaxEta = cms.untracked.vdouble(1000.0, 1000.0),
    MinEta = cms.untracked.vdouble(-1000.0, -1000.0),
    MinInvMass = cms.untracked.double(0.0),
    MaxInvMass = cms.untracked.double(100.0),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)



oniafilter = cms.EDFilter("PythiaFilter",
    Status = cms.untracked.int32(2),
    MaxEta = cms.untracked.double(1000.0),
    MinEta = cms.untracked.double(-1000.0),
    MinPt = cms.untracked.double(0.0),
    ParticleID = cms.untracked.int32(443)
)

ProductionFilterSequence = cms.Sequence(generator*oniafilter*mumugenfilter)
