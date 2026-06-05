#Pythia fragment for filtered Bc3P1 -> Bc(J/psi(mu+mu-)pi)gamma at 13.6TeV.   {Bc(3P1)}
#author: jhovanny.andres.mejia.guisao@cern.ch 

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(True),
                         comEnergy = cms.double(13600.),
                         ExternalDecays = cms.PSet(
                           EvtGen130 = cms.untracked.PSet(
                             # decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                             decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2020_NOLONGLIFE.DEC'),
                             particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_Bc_2014.pdl'),
                             #particle_property_file = cms.FileInPath('evt_Bc_2026.pdl'), ### CHECK ?!
                             convertPythiaCodes = cms.untracked.bool(False),
                             user_decay_embedded= cms.vstring(
"""
Particle B_c+       6.27447 0.00000e+00
Particle B_c*+      6.33207 0.00000e+00
Particle B_c1+      6.75000 0.00000
Particle B_c0*+     6.70600 0.00000e+00
Particle B_c2*+     6.76800 0.00000
Particle B_c-       6.27447 0.00000e+00
Particle B_c*-      6.33207 0.00000e+00
Particle B_c1-      6.75000 0.00000
Particle B_c0*-     6.70600 0.00000e+0
Particle B_c2*-     6.76800 0.00000
Particle J/psi      3.09690 9.29000e-05
Alias B_c+_SIGNAL B_c+
Alias B_c-_SIGNAL B_c-
Alias MyJ/psi J/psi
ChargeConj B_c+_SIGNAL B_c-_SIGNAL
ChargeConj B_c*+ B_c*-
ChargeConj B_c1+ B_c1-
ChargeConj B_c2*+ B_c2*-
ChargeConj MyJ/psi MyJ/psi

Decay B_c1+
  0.88 B_c+_SIGNAL gamma  PHSP;
  0.12 B_c*+       gamma  PHSP;
Enddecay
CDecay B_c1-

Decay B_c0*+
  1.0 B_c*+        gamma  PHSP;
Enddecay
CDecay B_c0*-

Decay B_c2*+
  1.0 B_c*+        gamma  PHSP;
Enddecay
CDecay B_c2*-

Decay B_c*+
  1.0 B_c+_SIGNAL  gamma   VSP_PWAVE;
Enddecay
CDecay B_c*-

Decay B_c+_SIGNAL
  1.0   MyJ/psi    pi+    SVS;
Enddecay
CDecay B_c-_SIGNAL

Decay MyJ/psi
  1.0   mu+  mu-            PHOTOS  VLL;
Enddecay
End
"""                             ),
                             operates_on_particles = cms.vint32(10543,10541,545),
                            # list_forced_decays = cms.vstring('MyBc+','MyBc-'),
                           ),
                           parameterSets = cms.vstring('EvtGen130')
                         ),
                         PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           processParameters = cms.vstring( # put below any needed pythia parameter
#
            '10543:m0 = 6.75000',        # Actualizamos la masa en Pythia para que coincida con EvtGen
            '10543:mWidth = 0.00000',    # Actualizamos el Width en Pythia para que coincida con EvtGen
            '10543:mMin = 6.75000',      # Ajustamos el umbral mínimo de masa
            '10543:mMax = 6.75000',      # Ajustamos el umbral máximo de masa
            '10543:oneChannel = 1 0.88 0 541 22',
            '10543:addChannel = 1 0.12 0 543 22',
            '10543:mayDecay = off',      # ¡IMPORTANTE! Le prohibimos a Pythia decaerla...
                               
#
            '10541:m0 = 6.70600',
            '10541:mWidth = 0.00000',                   
            '10541:mMin = 6.70600',      
            '10541:mMax = 6.70600',
            '10541:oneChannel = 1 1.0 0 543 22',
            '10541:mayDecay = off',                                                       
#
            '545:m0 = 6.76800',
            '545:mWidth = 0.00000',                   
            '545:mMin = 6.76800',      
            '545:mMax = 6.76800',
            '545:oneChannel = 1 1.0 0 543 22',
            '545:mayDecay = off',                        
#
            '543:m0 = 6.33207',
            '543:tau0 = 0.',
            '543:mayDecay = off',
#
            '541:m0 = 6.27447',
            '541:tau0 = 0.153',
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

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

bc2sgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(22),
    MaxEta = cms.untracked.vdouble(1.6),
    MinEta = cms.untracked.vdouble(-1.6),
    MinPt = cms.untracked.vdouble(0.25),
    NumberDaughters = cms.untracked.int32(1),
#    ParticleID = cms.untracked.int32(10543),                             
#    ParticleID = cms.untracked.int32(10541),                             
    ParticleID = cms.untracked.int32(545),                             
    verbose = cms.untracked.int32(0)
)

bcgenfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(211),
    MaxEta = cms.untracked.vdouble(2.6),
    MinEta = cms.untracked.vdouble(-2.6),
    MinPt = cms.untracked.vdouble(1.2),
    NumberDaughters = cms.untracked.int32(1),
    ParticleID = cms.untracked.int32(541),
    verbose = cms.untracked.int32(0)
)

jpsifilter = cms.EDFilter("PythiaDauVFilter",
  verbose         = cms.untracked.int32(0),
  NumberDaughters = cms.untracked.int32(2),
  MotherID        = cms.untracked.int32(541),
  ParticleID      = cms.untracked.int32(443),
  DaughterIDs     = cms.untracked.vint32(13, -13),
  MinPt           = cms.untracked.vdouble(2.8, 2.8),
  MinEta          = cms.untracked.vdouble(-2.6, -2.6),
  MaxEta          = cms.untracked.vdouble( 2.6,  2.6)
)

ProductionFilterSequence = cms.Sequence(generator*bc2sgenfilter*bcgenfilter*jpsifilter)
