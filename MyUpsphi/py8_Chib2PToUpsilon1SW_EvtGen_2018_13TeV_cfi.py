# cfg file for Chi_{b1}(2P) -> Upsilon(1S)W,  we are neglecting Chi_b0. Masses and widths are matched between pythia, evtgen and PDG 2024

#Pythia fragment for filtered Chi_{b1}(2P) -> Upsilon(mu+mu-) W(pi+pi-pi0) at 13.0TeV
#author: Jhovanny Andres Mejia
#email: jhovanny.andres.mejia.guisao@cern.ch

## note, the EvtOmegaDalitz is take form here: https://evtgen.hepforge.org/doc/models.html

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('mychi_b1'),    # will force one at the time
            operates_on_particles = cms.vint32(20553),          # we care just about our signal particles
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Particle Upsilon 9.4604000 0.00005402
Particle chi_b1  10.255460 0.00000

Alias      MyW  omega
Alias      myUpsilon Upsilon
Alias mychi_b1  chi_b1

Decay MyW
  1.0  pi+ pi- pi0       OMEGA_DALITZ;
Enddecay

Decay myUpsilon
  1.0  mu+  mu-          PHOTOS  VLL;
Enddecay

Decay mychi_b1
  1.0  MyW  myUpsilon  PHSP;
Enddecay

End
"""
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3PJ) = 20553',
            'Bottomonium:O(3PJ)[3P0(1)] = 0.085',
            'Bottomonium:O(3PJ)[3S1(8)] = 0.04',
            'Bottomonium:gg2bbbar(3PJ)[3PJ(1)]g = on',
            'Bottomonium:qg2bbbar(3PJ)[3PJ(1)]q = on',
            'Bottomonium:qqbar2bbbar(3PJ)[3PJ(1)]g = on',
            'Bottomonium:gg2bbbar(3PJ)[3S1(8)]g = on',
            'Bottomonium:qg2bbbar(3PJ)[3S1(8)]q = on',
            'Bottomonium:qqbar2bbbar(3PJ)[3S1(8)]g = on',
#            
            'PhaseSpace:pTHatMin = 2.',
#            
            '20553:m0 = 10.255460',
            '20553:mayDecay = off',       ## Pythia generates the particle but does not decay it, EvtGen will take care of that.
#            
            #'555:onMode = off',          ## Turn off all decays
            #"'20553:onIfMatch = 553 333' ## Enable only Upsilon phi decay 
#            
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

# We will filter for chi_b1 first on the ID, then in the mass.

pwaveIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(20553),
    MinPt = cms.untracked.vdouble(0.0),
    MinEta = cms.untracked.vdouble(-9.0),
    MaxEta = cms.untracked.vdouble(9.0),
    Status = cms.untracked.vint32(2)
)

upsIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(553),
    MinPt = cms.untracked.vdouble(9.0),
    MinEta = cms.untracked.vdouble(-1.6),
    MaxEta = cms.untracked.vdouble(1.6),
    Status = cms.untracked.vint32(2)
)

# Next two muon filter are derived from muon reconstruction

muminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20553),
    ParticleID = cms.untracked.int32(553),
    NumberDaughters = cms.untracked.int32(1),                             
    DaughterIDs = cms.untracked.vint32(-13),
    MinPt = cms.untracked.vdouble(3.0),                             
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

muplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20553),
    ParticleID = cms.untracked.int32(553),
    NumberDaughters = cms.untracked.int32(1),                            
    DaughterIDs = cms.untracked.vint32(13),                            
    MinPt = cms.untracked.vdouble(3.0),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

#  pion filters

piminusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20553),
    ParticleID = cms.untracked.int32(223),
    NumberDaughters = cms.untracked.int32(1),                             
    DaughterIDs = cms.untracked.vint32(-211),                             
    MinPt = cms.untracked.vdouble(0.5),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

piplusfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20553),
    ParticleID = cms.untracked.int32(223),                            
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(211),                        
    MinPt = cms.untracked.vdouble(0.5),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

pizerofilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(20553),
    ParticleID = cms.untracked.int32(223),                            
    NumberDaughters = cms.untracked.int32(1),
    DaughterIDs = cms.untracked.vint32(111),                        
    MinPt = cms.untracked.vdouble(0.2),
    ChargeConjugation = cms.untracked.bool(False),
    MinEta = cms.untracked.vdouble(-2.5),
    MaxEta = cms.untracked.vdouble(2.5)
)

ProductionFilterSequence = cms.Sequence(generator*pwaveIDfilter*upsIDfilter*piminusfilter*piplusfilter*pizerofilter*muminusfilter*muplusfilter)
