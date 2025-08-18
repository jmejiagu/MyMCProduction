import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

_generator = cms.EDFilter("Pythia8GeneratorFilter",
                         comEnergy = cms.double(13600.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            user_decay_embedded = cms.vstring(
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
'Particle   B0            5.2796300e+00   0.0000000e+00',
'Particle   anti-B0       5.2796300e+00   0.0000000e+00',
'Particle   B_s0          5.3668900e+00   0.0000000e+00',
'Particle   anti-B_s0     5.3668900e+00   0.0000000e+00',
'Particle   J/psi         3.0969000e+00   9.2900006e-05',
'Particle   Xi-           1.3217100e+00   0.0000000e+00',
'Particle   anti-Xi+      1.3217100e+00   0.0000000e+00',
'Particle   psi(2S)       3.6860970e+00   2.9400000e-04',
'Particle   Xi_b-         5.7970000e+00   0.0000000e+00',
'Particle   anti-Xi_b+    5.7970000e+00   0.0000000e+00',
'#',
'Alias      MyXi_b-        Xi_b-',
'Alias      Myanti-Xi_b+   anti-Xi_b+',
'ChargeConj Myanti-Xi_b+   MyXi_b-',
'#',
'Decay MyXi_b-',
'1.000  mu+     mu-    Xi-    PHSP;',
'Enddecay',
'CDecay Myanti-Xi_b+',
'End'
),
            list_forced_decays = cms.vstring('MyXi_b-','Myanti-Xi_b+'),
            operates_on_particles = cms.vint32(),
            convertPythiaCodes = cms.untracked.bool(False)
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            "SoftQCD:nonDiffractive = on",
            "5132:m0=5.7970",       ## changing also Xi_b- mass in pythia
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

from GeneratorInterface.Core.ExternalGeneratorFilter import ExternalGeneratorFilter
generator = ExternalGeneratorFilter(_generator)

###########
# Filters #
###########

#
xibfilter = cms.EDFilter("PythiaFilter", ParticleID = cms.untracked.int32(5132))

decayfilter = cms.EDFilter("PythiaDauVFilter",
    DaughterIDs = cms.untracked.vint32(13, -13, 3312),
    MaxEta = cms.untracked.vdouble(0.0, 0.0, 9999.9),
    MinEta = cms.untracked.vdouble(-0.0, -0.0, -9999.9),
    MinPt = cms.untracked.vdouble(0.0, 0.0, 0.0),
    NumberDaughters = cms.untracked.int32(3),
    ParticleID = cms.untracked.int32(5132),
    verbose = cms.untracked.int32(1)
)

ProductionFilterSequence = cms.Sequence(generator*xibfilter*decayfilter)
