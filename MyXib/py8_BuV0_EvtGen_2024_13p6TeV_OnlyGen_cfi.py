import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         comEnergy = cms.double(13600.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_embedded= cms.vstring(
'#',
'Particle   pi+           1.3957061e-01   0.0000000e+00',
'Particle   pi-           1.3957061e-01   0.0000000e+00',
'Particle   K_S0          4.9761100e-01   0.0000000e+00',
'Particle   K*+           8.9176000e-01   5.0300000e-02',
'Particle   K*-           8.9176000e-01   5.0300000e-02',
'Particle   K*0           8.9555000e-01   4.7300000e-02',
'Particle   anti-K*0      8.9555000e-01   4.7300000e-02',
'Particle   rho0          7.7526000e-01   1.4910000e-01',
'Particle   phi           1.0194610e+00   4.2490000e-03',
'Particle   B-            5.2793200e+00   0.0000000e+00',
'Particle   B+            5.2793200e+00   0.0000000e+00',
'Particle   B*+           5.3247700e+00   0.0000000e+00', ## 5279.32 + 45.45 523
'Particle   B*-           5.3247700e+00   0.0000000e+00',                
'Particle   B0            5.2796300e+00   0.0000000e+00',
'Particle   anti-B0       5.2796300e+00   0.0000000e+00',
'Particle   B_s0          5.3668900e+00   0.0000000e+00',
'Particle   anti-B_s0     5.3668900e+00   0.0000000e+00',
'Particle   J/psi         3.0969000e+00   9.2900006e-05',
'Particle   Xi-           1.3217100e+00   0.0000000e+00', ## id 3312
'Particle   anti-Xi+      1.3217100e+00   0.0000000e+00',
'Particle   psi(2S)       3.6860970e+00   2.9400000e-04',
'Particle   Xi_b-         5.7970000e+00   0.0000000e+00', ## mass = PDG 2022
'Particle   anti-Xi_b+    5.7970000e+00   0.0000000e+00', ## id 5132
'#',
'Particle   Sigma_b-      6.4860000e+00    6.4160000e-02', ## esmatimated mass and width from PHYSICAL REVIEW D 100, 094032 (2019)
'Particle   anti-Sigma_b+ 6.4860000e+00    6.4160000e-02', ## id 5112                
'#',
'Alias      MyXi_BV-         Sigma_b-',
'Alias      Myanti-Xi_BV+    anti-Sigma_b+',
'ChargeConj Myanti-Xi_BV+    MyXi_BV-',
'#',
'Alias      MyB+   B+',
'Alias      MyB-   B-',
'ChargeConj MyB-   MyB+',
'#',               
'Alias      MyB*+            B*+',
'Alias      MyB*-            B*-',
'ChargeConj MyB*-            MyB*+',                
'#',
'Alias      MyLambda0         Lambda0',
'Alias      Myanti-Lambda0    anti-Lambda0',
'ChargeConj MyLambda0         Myanti-Lambda0',               
'#',
'Alias       Mypsi      J/psi',
'ChargeConj  Mypsi      Mypsi',
'#',
'Decay MyLambda0',
' 1.000     p+       pi-              PHSP;',
'Enddecay',
'CDecay Myanti-Lambda0',
'#',                
'Decay Mypsi',
' 1.000     mu+       mu-       PHOTOS VLL;',
'Enddecay',
'#',
'Decay MyB+',
'  1.000    MyJpsi      K+             SVS;',
'Enddecay',
'CDecay MyB-',                
'#',
'Decay MyB*+',
'1.000     MyB+         gamma    VSP_PWAVE;',
'Enddecay',
'CDecay MyB*-',
'#',                
'Decay MyXi_BV-',
' 0.55    MyB-    MyLambda0         PHSP;',
' 0.45    MyB*-   MyLambda0         PHSP;',      
'Enddecay',
'CDecay Myanti-Xi_BV+',                
'End'
), 
            list_forced_decays = cms.vstring('MyXi_BV-','Myanti-Xi_BV+'),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False)
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',
 #           
            '5112:m0=6.486',       ## changing also Sigma_b- mass in pythia
            '5112:mWidth = 0.06416',    # We updated the Width in Pythia to match EvtGen.
            '5112:oneChannel = 1 0.55 0 521 3122',
            '5112:addChannel = 1 0.45 0 523 3122',
            '5112:mayDecay = off',      # ¡IMPORTANT! We forbid Pythia to decay it...
#
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0'),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

#from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
#generator = ExternalGeneratorFilter(_generator)

###########
# Filters #
###########

#xibfilter = cms.EDFilter("PythiaFilter", ParticleID = cms.untracked.int32(5112))
xibfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(3122),
    MinRapidity = cms.untracked.double(-2.6),
    MaxRapidity = cms.untracked.double(2.6),                     
    MinPt = cms.untracked.vdouble(1.0),                         
    NumberDaughters = cms.untracked.int32(1),
    ParticleID = cms.untracked.int32(5112),
    verbose = cms.untracked.int32(0)
)

bfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(521),
    MinRapidity = cms.untracked.double(-2.5),
    MaxRapidity = cms.untracked.double(2.5),
    MinPt = cms.untracked.double(9.0),
    MaxPt = cms.untracked.double(1000.0),
)

bugenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(321),
    MaxEta = cms.untracked.vdouble(2.6),
    MinEta = cms.untracked.vdouble(-2.6),
    MinPt = cms.untracked.vdouble(1.1),
    NumberDaughters = cms.untracked.int32(1),
    ParticleID = cms.untracked.int32(521),
    verbose = cms.untracked.int32(0)
)

jpsifilter = cms.EDFilter("PythiaDauVFilter",
  verbose         = cms.untracked.int32(0),
  NumberDaughters = cms.untracked.int32(2),
  MotherID        = cms.untracked.int32(521),
  ParticleID      = cms.untracked.int32(443),
  DaughterIDs     = cms.untracked.vint32(13, -13),
  MinPt           = cms.untracked.vdouble(2.0, 2.0),
  MinEta          = cms.untracked.vdouble(-2.6, -2.6),
  MaxEta          = cms.untracked.vdouble( 2.6,  2.6)
)

ProductionFilterSequence = cms.Sequence(generator*xibfilter*bfilter*bugenfilter*jpsifilter)
