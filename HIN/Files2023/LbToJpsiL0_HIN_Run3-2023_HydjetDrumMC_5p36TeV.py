#Pythia fragment for filtered B0 -> J/psi(mu+mu-)Kshort(pi+pi-) at 5.36TeV
#author: jhovanny.andres.mejia.guisao@cern.ch
#For 2018
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIN-HINPbPbAutumn18GSHIMix-00005
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/HIN-HiFall15-00043
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/BPH-Run3Summer22EEGS-00107
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/BPH-RunIISummer15GS-00163
#For 2023
#EXAMPLE TAKEN FROM https://gitlab.cern.ch/cms-hin-pag/ping-forward-upc/mcrequest/-/tree/master/PYTHIA8_Fragments
#EXAMPLE TAKEN FROM https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/BPH-Run3Summer23GS-00122 

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
# This is the decay file for the decay B0 -> J/psi(->mumu) Kshort(->pipi)
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
1.000  MyLambda  MyJpsi  HELAMP 1 0 0.129 -2.523 1.021 1.122 0.145 1.788;
Enddecay
Decay MyantiLambdab0
1.000  MyLambdabar  MyJpsi  HELAMP 1 0 0.129 -2.523 1.021 1.122 0.145 1.788;
Enddecay
#
#
Decay MyLambda
1.000   p+  pi-  LAMBDA2PPIFORLAMBDAB2LAMBDAV 0 1; 
Enddecay
#
Decay MyLambdabar
1.000   anti-p-  pi+  LAMBDA2PPIFORLAMBDAB2LAMBDAV 0 1;
Enddecay
#
Decay MyJpsi
  1.000         mu+       mu-         PHOTOS VLL;
Enddecay
#
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
    MinPt           = cms.untracked.vdouble(-1., -1),
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

lambdafilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(5122),
    ParticleID      = cms.untracked.int32(3122),
    DaughterIDs     = cms.untracked.vint32(2212, -211),
    MinPt           = cms.untracked.vdouble(0.25, 0.25),
    MinEta          = cms.untracked.vdouble(-3.0, -3.0),
    MaxEta          = cms.untracked.vdouble( 3.0, 3.0)
    )

ProductionFilterSequence = cms.Sequence(generator*decayfilter*jpsifilter*lambdafilter)
