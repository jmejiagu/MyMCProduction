#Pythia fragment for filtered Bc -> chicK -> J/psi(mu+mu-)gammaK at 13.6TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/ChiProduction/py8_BuChic1K_EvtGen_TuneCUETP8M1_13TeV_cfi.py

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bc_2014.pdl'),
            #list_forced_decays = cms.vstring('B_c+_SIGNAL','B_c-_SIGNAL'),
            #operates_on_particles = cms.vint32(541,-541),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for Bc->Chi_c{1,2}(Jpsi ( -> mu mu ) gamma) pi+
#
Particle B_c+      6.27490 0.00000

Alias      MyJ/psi          J/psi
Alias      Mychi_c0         chi_c0
Alias      Mychi_c1         chi_c1
Alias      Mychi_c2         chi_c2
Alias      B_c+_SIGNAL      B_c+
Alias      B_c-_SIGNAL B_c-
ChargeConj B_c+_SIGNAL B_c-_SIGNAL

Decay MyJ/psi  # original total forced BR = 0.05930000
 1.0000  mu+     mu-          PHOTOS  VLL;
Enddecay

Decay Mychi_c0  # original total forced BR = 0.01160000
 1.0000  MyJ/psi    gamma     PHSP;
Enddecay

Decay Mychi_c1  # original total forced BR = 0.34400000
 1.0000  MyJ/psi  gamma      VVP 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0;
Enddecay

Decay Mychi_c2  # original total forced BR = 0.19500000
 1.0000  MyJ/psi  gamma     PHSP;
Enddecay

Decay B_c+_SIGNAL  # original total forced BR = LHCB paper??
 0.5000  Mychi_c1 pi+       SVS;
 0.5000  Mychi_c2 pi+       STS;
Enddecay
CDecay B_c-_SIGNAL

End
"""
            ),
            operates_on_particles = cms.vint32(541,-541), 
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

#from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
#generator = ExternalGeneratorFilter(_generator)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

###### Filters ##########

jpsi_from_b_hadron_filter = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    DaughterMaxEtas = cms.untracked.vdouble(2.52, 2.52),
    DaughterMaxPts = cms.untracked.vdouble(1000000.0, 1000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.52, -2.52),
    DaughterMinPts = cms.untracked.vdouble(3.8, 3.8),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(6.0),
    MotherIDs = cms.untracked.vint32(541),
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
    DaughterMinPts = cms.untracked.vdouble(3.8, 3.8),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(6.0),
    MotherIDs = cms.untracked.vint32(445, 20443),
    ParticleID = cms.untracked.int32(443)
)

ProductionFilterSequence = cms.Sequence(generator*jpsi_from_b_hadron_filter*jpsi_from_ancestor*gammafilter)
