#Pythia fragment for filtered Bu -> chicK -> J/psi(mu+mu-)gammaK at 13.6TeV
#author: Alberto sanchez
#edited by: jhovanny.andres.mejia.guisao@cern.ch
#TAKEN FROM https://github.com/alberto-sanchez/my-genproductions/blob/master/ChiProduction/py8_BuChic1K_EvtGen_TuneCUETP8M1_13TeV_cfi.py
# OTHER EXAMPLE: https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=XibToJpsiLambdaK_JMM_MMFilter_DGamma0_TuneCP5_13TeV-pythia8-evtgen&page=-1&shown=127

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *


_generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
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
# This is the decay file for B->Chi_c{1,2}(Jpsi ( -> mu mu ) gamma) K+
#
Alias      MyJ/psi          J/psi
Alias      Mychi_c0         chi_c0
Alias      Mychi_c1         chi_c1
Alias      Mychi_c2         chi_c2
Alias      MyB+             B+
Alias      MyB-             B-
ChargeConj MyB-             MyB+

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

Decay MyB+  # original total forced BR = 0.01756960
 0.5000  Mychi_c1 K+       SVS;
 0.5000  Mychi_c2 K+       STS;
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
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

_generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)
from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)

#from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
#generator = ExternalGeneratorFilter(_generator)
#generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

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
    DaughterMinPts = cms.untracked.vdouble(3.8, 3.8),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(6.0),
    MotherIDs = cms.untracked.vint32(445, 20443),
    ParticleID = cms.untracked.int32(443)
)



ProductionFilterSequence = cms.Sequence(generator*jpsi_from_b_hadron_filter*jpsi_from_ancestor*gammafilter)
