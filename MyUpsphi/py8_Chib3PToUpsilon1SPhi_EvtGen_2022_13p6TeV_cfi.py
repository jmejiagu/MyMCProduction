# cfg file for Chi_{b1,b2}(3P) -> Upsilon(1S) phi,  we are neglecting Chi_b0. Masses and widths are matched between pythia, evtgen and PDG 2024
# a mass separation between Chi_b1 and Chi_b2 is assumed to be 10.60 MeV  
# ##https://github.com/alberto-sanchez/my-genproductions/blob/master/ChiProduction/py8_Chib3PToUpsilon1SGamma_EvtGen_TuneCUETP8M1_13TeV_cfi.py

#Pythia fragment for filtered Chi_{b1,b2}(3P) -> Upsilon(mu+mu-) phi(k+k-) at 13.6TeV
#author: Jhovanny Andres Mejia
#email: jhovanny.andres.mejia.guisao@cern.ch

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('mychi_b1','mychi_b2'),    # will force one at the time
            operates_on_particles = cms.vint32(20553,555),          # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Particle Upsilon 9.4604000 0.00005402
Particle chi_b1  10.513400 0.00000
Particle chi_b2  10.524000 0.00000

Alias      MyPhi  phi
Alias      myUpsilon Upsilon
Alias mychi_b1  chi_b1(3P)
Alias mychi_b2  chi_b2(3P)

Decay MyPhi
  1.000         K+          K-           VSS;
Enddecay

Decay myUpsilon
1.0   mu+  mu-          PHOTOS  VLL;
Enddecay

Decay mychi_b1
1.0   MyPhi  myUpsilon  PHSP;
Enddecay

Decay mychi_b2
1.0   MyPhi  myUpsilon  PHSP;
Enddecay

End
"""
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3PJ) = 20553,555',
            'Bottomonium:O(3PJ)[3P0(1)] = 0.085,0.085',
            'Bottomonium:O(3PJ)[3S1(8)] = 0.04,0.04',
            'Bottomonium:gg2bbbar(3PJ)[3PJ(1)]g = on,on',
            'Bottomonium:qg2bbbar(3PJ)[3PJ(1)]q = on,on',
            'Bottomonium:qqbar2bbbar(3PJ)[3PJ(1)]g = on,on',
            'Bottomonium:gg2bbbar(3PJ)[3S1(8)]g = on,on',
            'Bottomonium:qg2bbbar(3PJ)[3S1(8)]q = on,on',
            'Bottomonium:qqbar2bbbar(3PJ)[3S1(8)]g = on,on',
#            
            'PhaseSpace:pTHatMin = 2.',
#            
            '20553:m0 = 10.513400',
            '20553:mayDecay = off',       ## Pythia generates the particle but does not decay it, EvtGen will take care of that.
#            
            '555:m0 = 10.524000',
            '20553:mayDecay = off'
#            
            #'555:onMode = off',          ## Turn off all decays
            #"'20553:onIfMatch = 553 333' ## Enable only Upsilon phi decay 
            #'555:onMode = off'
#            
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

# We will filter for chi_b1, and chi_b2, first on the ID, then in the mass.

pwaveIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(20553,555),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    MinEta = cms.untracked.vdouble(-9., -9.),
    MaxEta = cms.untracked.vdouble(9., 9.),
    Status = cms.untracked.vint32(2, 2)
)

pwaveMassfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(2, 2),
    MinPt = cms.untracked.vdouble(9., 0.5),
    MaxEta = cms.untracked.vdouble(9., 9.),
    MinEta = cms.untracked.vdouble(-9., -9.),
    ParticleCharge = cms.untracked.int32(0),
    MinP = cms.untracked.vdouble(0.,0.),
    ParticleID1 = cms.untracked.vint32(553),
    ParticleID2 = cms.untracked.vint32(333),
    MinInvMass = cms.untracked.double(10.51),
    MaxInvMass = cms.untracked.double(10.53),
)

# Next two filter are derived from the reconstruction (https://indico.cern.ch/event/1503216/)

Upsi_from_ancestor = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-13, 13),
    DaughterMaxEtas = cms.untracked.vdouble(2.5, 2.5),
    DaughterMaxPts = cms.untracked.vdouble(1000000.0, 1000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.5, -2.5),
    DaughterMinPts = cms.untracked.vdouble(3.0, 3.0),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(9.0),
    MotherIDs = cms.untracked.vint32(20553,555),
    ParticleID = cms.untracked.int32(553)
)

phi_from_ancestor = cms.EDFilter("PythiaFilterMultiAncestor",
    DaughterIDs = cms.untracked.vint32(-321, 321),
    DaughterMaxEtas = cms.untracked.vdouble(2.5, 2.5),
    DaughterMaxPts = cms.untracked.vdouble(1000000.0, 1000000.0),
    DaughterMinEtas = cms.untracked.vdouble(-2.5, -2.5),
    DaughterMinPts = cms.untracked.vdouble(0.5, 0.5),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(0.5),
    MotherIDs = cms.untracked.vint32(20553,555),
    ParticleID = cms.untracked.int32(333)
)


ProductionFilterSequence = cms.Sequence(generator*pwaveIDfilter*pwaveMassfilter*Upsi_from_ancestor*phi_from_ancestor)
