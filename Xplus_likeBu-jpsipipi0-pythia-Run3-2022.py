#Pythia fragment for filtered X+(3872) -> J/psi(mu+mu-)pi+pi0(gammagamma) at 13.6TeV
#author: Jhovanny Andres Mejia
#email: jhovanny.andres.mejia.guisao@cern.ch

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),                     
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13600.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#10020443
# Particles updated from PDG2024 https://pdglive.lbl.gov/Viewer.action
# This is the decay file for X(3872)+->Jpsi(mu+mu-)pi+pi0(gammagamma)
#
Particle   J/psi       3.0969000e+00   9.2600000e-05 ## 443
Particle   B+          3.8716400e+00   0.0000  0.0000    3   2  0.0000000e-00
Particle   B-          3.8716400e+00   0.0000  0.0000    -3  2  0.0000000e-00   ## 521 with X mass width=0.00119?? and spin=1 and lifetime=0.0

Alias      MyX(3872)+       B+
Alias      MyAntiX(3872)-   B-
ChargeConj MyAntiX(3872)-   MyX(3872)+

Alias      MyJ/psi     J/psi
ChargeConj MyJ/psi     MyJ/psi

Decay MyX(3872)+
1.000   MyJ/psi  pi+  pi0     PHSP;
Enddecay
CDecay MyAntiX(3872)-

Decay pi0
 1.000   gamma   gamma       PHSP;  ## VSP_PWAVE??
Enddecay

Decay MyJ/psi
 1.0000  mu+     mu-         PHOTOS  VLL;
Enddecay

End
"""
            ),
            operates_on_particles = cms.vint32(521,-521), 
            list_forced_decays = cms.vstring('MyX(3872)+','MyAntiX(3872)-'),  
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring( # put below any needed pythia parameter

            ### https://www.pythia.org/latest-manual/Welcome.html
            ### https://pythia.org/latest-manual/ParticleDataScheme.html

            '521:m0 = 3.87164',
            '521:tau0 = 0.0',
            '521:mWidth = 0.0',
            '521:spinType = 3.0',
            '521:mayDecay = off',

            '541:m0 = 6.27447', ## Bc mass
            '541:tau0 = 0.151995', ## Bc lifetime in c*tau/mm 
            '5122:m0 = 5.61960', ## Lb mass 
            '5122:tau0 = 0.439', ## Lb lifetime in c*tau/mm 299792458*1000* 0.964*1519*10^(-15)
            '5232:m0 = 5.7919', ## Xib0 mass 
            '5232:tau0 = 0.428', ## Xib0 lifetime in c*tau/mm 299792458*1000* 0.964*1480*10^(-15)
            '5132:m0 = 5.7970', ## Xib- mass 
            '5132:tau0 = 0.454', ## Xib- lifetime in c*tau/mm 299792458*1000* 0.964*1572*10^(-15)
            '5132:m0 = 6.0452', ## Omegab- mass 
            '5132:tau0 = 0.474', ## Omegab- lifetime in c*tau/mm 299792458*1000* 0.964*1640*10^(-15)
            '443:m0=3.0969',    ## Jpsi
#            '20443:m0=3.51067', ## chi_c1 mass 
#            '20443:mMin=3.50167', ## 
#            '20443:mMax=3.52067', ## 
#            '20443:mWidth=0.00084', ## changing chi_c1 with to match X(3872)
#            'Charmonium:states(3PJ) = 20443,445',   # is it better to generating only Chi_c1 particle (20443)??
#            'Charmonium:O(3PJ)[3P0(1)] = 0.05,0.05',
#            'Charmonium:O(3PJ)[3S1(8)] = 0.0031,0.0031',
#            'Charmonium:gg2ccbar(3PJ)[3PJ(1)]g = on,on',
#            'Charmonium:qg2ccbar(3PJ)[3PJ(1)]q = on,on',
#            'Charmonium:qqbar2ccbar(3PJ)[3PJ(1)]g = on,on',
#            'Charmonium:gg2ccbar(3PJ)[3S1(8)]g = on,on',
#            'Charmonium:qg2ccbar(3PJ)[3S1(8)]q = on,on',
#            'Charmonium:qqbar2ccbar(3PJ)[3S1(8)]g = on,on',
#            'Charmonium:states(3P1) = 20443',
            
#            'PhaseSpace:pTHatMin = 5.', 
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 4', # PDG id of q quark
            'PTFilter:scaleToFilter = 1.0',
#           'PTFilter:quarkPtMin = 1.0',  # Mínimo pT en GeV
#           'PTFilter:quarkPtMax = 20.0', # Máximo pT en GeV (optional)
#
            #'ProcessLevel:all = off',
            #'ProcessLevel:resonanceDecays = on'
            'HardQCD:gg2ccbar = on',
            'HardQCD:qqbar2ccbar = on',
            'HardQCD:hardccbar = on',
            "SoftQCD:nonDiffractive = on",
            #'HardQCD:all = on',
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

xxfilter = cms.EDFilter("PythiaDauVFilter",
        NumberDaughters = cms.untracked.int32(3),
        ParticleID      = cms.untracked.int32(521),  
        DaughterIDs     = cms.untracked.vint32(443, 211, 111),
        MinPt           = cms.untracked.vdouble(6.0, 0.2, 0.05), 
        MinEta          = cms.untracked.vdouble(-5.0, -9999.0, -9999.0), 
        MaxEta          = cms.untracked.vdouble( 5.0,  9999.0, 9999.0),
        verbose = cms.untracked.int32(0)                
)

photonfilter = cms.EDFilter("PythiaDauVFilter",
            NumberDaughters = cms.untracked.int32(2),
            MotherID        = cms.untracked.int32(521),
            ParticleID      = cms.untracked.int32(111),
            DaughterIDs     = cms.untracked.vint32(22, 22),
            MinPt           = cms.untracked.vdouble(0.0, 0.0),
            MinEta          = cms.untracked.vdouble(-9999.0, -9999.0),
            MaxEta          = cms.untracked.vdouble( 9999.0,  9999.0),
            verbose = cms.untracked.int32(0)                
        )

jmmfilter = cms.EDFilter("PythiaDauVFilter",
            NumberDaughters = cms.untracked.int32(2),
            MotherID        = cms.untracked.int32(521),
            ParticleID      = cms.untracked.int32(443),
            DaughterIDs     = cms.untracked.vint32(13, -13),
            MinPt           = cms.untracked.vdouble(3.0, 3.0),
            MinEta          = cms.untracked.vdouble(-2.6, -2.6),
            MaxEta          = cms.untracked.vdouble( 2.6,  2.6),
            verbose = cms.untracked.int32(0)             
        )

ProductionFilterSequence = cms.Sequence(generator*xxfilter*jmmfilter)
#ProductionFilterSequence = cms.Sequence(generator*xxfilter*photonfilter*jmmfilter)
