#Pythia fragment for filtered B0 -> J/psi(mu+mu-)Kshort(pi+pi-) at 5.02TeV
#author: jhovanny.andres.mejia.guisao@cern.ch
#for 2018
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIN-HINPbPbAutumn18GSHIMix-00005
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIN-HiFall15-00043
#For 2023
#EXAMPLE TAKEN FROM https://gitlab.cern.ch/cms-hin-pag/ping-forward-upc/mcrequest/-/tree/master/PYTHIA8_Fragments
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/BPH-Run3Summer23GS-00122


import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
#from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import * ## This was in 2018 silmulation, for 13.0 TeV
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
            list_forced_decays = cms.vstring('MyB0','Myanti-B0'),
            operates_on_particles = cms.vint32(511,-511),    # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay B0 -> J/psi(->mumu) Kshort(->pipi)
#
Alias      MyB0   B0
Alias      Myanti-B0   anti-B0
ChargeConj Myanti-B0   MyB0
Alias      MyJpsi      J/psi
ChargeConj MyJpsi      MyJpsi
Alias      MyK_S0      K_S0
ChargeConj MyK_S0      MyK_S0
#
Decay MyB0
1.000    MyJpsi      MyK_S0             SVS;
Enddecay
CDecay Myanti-B0
#
Decay MyJpsi
  1.000         mu+       mu-            PHOTOS VLL;
Enddecay
#
Decay MyK_S0
  1.000        pi+        pi-  PHSP;
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
            'PhaseSpace:pTHatMin = 2.',
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
    ParticleID      = cms.untracked.int32(511),
    DaughterIDs     = cms.untracked.vint32(443, 310),
    MinPt           = cms.untracked.vdouble(-1., -1),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999., 9999.)
    )

jpsifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(511),
    ParticleID      = cms.untracked.int32(443),
    DaughterIDs     = cms.untracked.vint32(13, -13),
    MinPt           = cms.untracked.vdouble(1.0, 1.0),
    MinEta          = cms.untracked.vdouble(-2.7, -2.7),
    MaxEta          = cms.untracked.vdouble( 2.7, 2.7)
    )

kshortfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(511),
    ParticleID      = cms.untracked.int32(310),
    DaughterIDs     = cms.untracked.vint32(211, -211),
    MinPt           = cms.untracked.vdouble(0.25, 0.25),
    MinEta          = cms.untracked.vdouble(-3.0, -3.0),
    MaxEta          = cms.untracked.vdouble( 3.0, 3.0)
    )



ProductionFilterSequence = cms.Sequence(generator*decayfilter*jpsifilter*kshortfilter)



