#Pythia fragment for filtered Bu -> chicK -> J/psi(mu+mu-)gammaK at 13.6TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/ChiProduction/py8_BuChic1K_EvtGen_TuneCUETP8M1_13TeV_cfi.py

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(True),
                         comEnergy = cms.double(13600.),
                         ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                             decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                             #user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bu_chic1K_jpsigammaK.dec'),
                             user_decay_file = cms.vstring('BplusSignal.dec'),  
                            list_forced_decays = cms.vstring('MyB+','MyB-'),
                            operates_on_particles = cms.vint32()
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            'PhaseSpace:pTHatMin = 8.',   
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

jpsi_from_b_hadron_filter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    DaughterMaxEtas = cms.untracked.vdouble(2.52, 2.52),
    DaughterMaxPts = cms.untracked.vdouble(1000000.0, 1000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.52, -2.52),
    DaughterMinPts = cms.untracked.vdouble(3.5, 3.5),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(5.0),
    MotherIDs = cms.untracked.vint32(521),
    ParticleID = cms.untracked.int32(443)
)

gammafilter = cms.EDFilter("MCMultiParticleFilter",
    AcceptMore = cms.bool(True),
    EtaMax = cms.vdouble(2.52, 2.52),
    MotherID = cms.untracked.vint32(445, 20443),
    NumRequired = cms.int32(1),
    ParticleID = cms.vint32(22, 22),
    PtMin = cms.vdouble(0.2, 0.2),
    Status = cms.vint32(1, 1)
)
 

jpsi_from_ancestor = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    DaughterMaxEtas = cms.untracked.vdouble(2.52, 2.52),
    DaughterMaxPts = cms.untracked.vdouble(1000000.0, 1000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.52, -2.52),
    DaughterMinPts = cms.untracked.vdouble(3.5, 3.5),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(5.0),
    MotherIDs = cms.untracked.vint32(445, 20443),
    ParticleID = cms.untracked.int32(443)
)



ProductionFilterSequence = cms.Sequence(generator*jpsi_from_b_hadron_filter*jpsi_from_ancestor*gammafilter)
