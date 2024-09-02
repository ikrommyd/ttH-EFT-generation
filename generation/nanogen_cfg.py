# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/pythia_fragment.py --python_filename nanogen_cfg.py --eventcontent NANOAODGEN --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=123 --fileout file:nanogen_123.root --conditions 130X_mcRun3_2023_realistic_v14 --beamspot Realistic25ns13p6TeVEarly2023Collision --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run3 --no_exec --mc -n 10000
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('NANOGEN',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13p6TeVEarly2023Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('PhysicsTools.NanoAOD.nanogen_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/pythia_fragment.py nevts:10000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODGENoutput = cms.OutputModule("NanoAODOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:nanogen_123.root'),
    outputCommands = process.NANOAODGENEventContent.outputCommands
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2023_realistic_v14', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('pythia8_example03'),
        pythia8_example03 = cms.vstring(
            'PartonLevel:ISR=off',
            'PartonLevel:FSR = off',
            'PartonLevel:MPI = off',
            'HadronLevel:all = off',
            'BeamRemnants:primordialKT = off'
        )
    ),
    comEnergy = cms.double(13600.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)


process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/uscms/home/ikrommyd/nobackup/ttH-EFT-generation/generation/genproductions/bin/MadGraph5_aMCatNLO/ttHtoGG_tutorial_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(10000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.pgen)
process.nanoAOD_step = cms.Path(process.nanogenSequence)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODGENoutput_step = cms.EndPath(process.NANOAODGENoutput)

# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.nanoAOD_step,process.endjob_step,process.NANOAODGENoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfConcurrentLuminosityBlocks = 1
process.options.eventSetup.numberOfConcurrentIOVs = 1
# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path).insert(0, process.generator)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nanogen_cff
from PhysicsTools.NanoAOD.nanogen_cff import customizeNanoGEN 

#call to customisation function customizeNanoGEN imported from PhysicsTools.NanoAOD.nanogen_cff
process = customizeNanoGEN(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions


# Customisation from command line

process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=123
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
named_weights = [
"rw0000",
"rw0001",
"rw0002",
"rw0003",
"rw0004",
"rw0005",
"rw0006",
"rw0007",
"rw0008",
"rw0009",
"rw0010",
"rw0011",
"rw0012",
"rw0013",
"rw0014",
"rw0015",
"rw0016",
"rw0017",
"rw0018",
"rw0019",
"rw0020",
"rw0021",
"rw0022",
"rw0023",
"rw0024",
"rw0025",
"rw0026",
"rw0027",
"rw0028",
"rw0029",
"rw0030",
"rw0031",
"rw0032",
"rw0033",
"rw0034",
"rw0035",
"rw0036",
"rw0037",
"rw0038",
"rw0039",
"rw0040",
"rw0041",
"rw0042",
"rw0043",
"rw0044",
"rw0045",
"rw0046",
"rw0047",
"rw0048",
"rw0049",
"rw0050",
"rw0051",
"rw0052",
"rw0053",
"rw0054",
"rw0055",
"rw0056",
"rw0057",
"rw0058",
"rw0059",
"rw0060",
"rw0061",
"rw0062",
"rw0063",
"rw0064",
"rw0065",
"rw0066",
"rw0067",
"rw0068",
"rw0069",
"rw0070",
"rw0071",
"rw0072",
"rw0073",
"rw0074",
"rw0075",
"rw0076",
"rw0077",
"rw0078",
"rw0079",
"rw0080",
"rw0081",
"rw0082",
"rw0083",
"rw0084",
"rw0085",
"rw0086",
"rw0087",
"rw0088",
"rw0089",
"rw0090",
"rw0091",
"rw0092",
"rw0093",
"rw0094",
"rw0095",
"rw0096",
"rw0097",
"rw0098",
"rw0099",
"rw0100",
"rw0101",
"rw0102",
"rw0103",
"rw0104",
"rw0105",
"rw0106",
"rw0107",
"rw0108",
"rw0109",
"rw0110",
"rw0111",
"rw0112",
"rw0113",
"rw0114",
"rw0115",
"rw0116",
"rw0117",
"rw0118",
"rw0119",
"rw0120",
"rw0121",
"rw0122",
"rw0123",
"rw0124",
"rw0125",
"rw0126",
"rw0127",
"rw0128",
"rw0129",
"rw0130",
"rw0131",
"rw0132",
"rw0133",
"rw0134",
"rw0135",
"rw0136",
"rw0137",
"rw0138",
"rw0139",
"rw0140",
"rw0141",
"rw0142",
"rw0143",
"rw0144",
"rw0145",
"rw0146",
"rw0147",
"rw0148",
"rw0149",
"rw0150",
"rw0151",
"rw0152",
"rw0153",
"rw0154",
"rw0155",
"rw0156",
"rw0157",
"rw0158",
"rw0159",
"rw0160",
"rw0161",
"rw0162",
"rw0163",
"rw0164",
"rw0165",
"rw0166",
"rw0167",
"rw0168",
"rw0169",
"rw0170",
"rw0171",
"rw0172",
"rw0173",
"rw0174",
"rw0175",
"rw0176",
"rw0177",
"rw0178",
"rw0179",
"rw0180",
"rw0181",
"rw0182",
"rw0183",
"rw0184",
"rw0185",
"rw0186",
"rw0187",
"rw0188",
"rw0189",
"rw0190",
"rw0191",
"rw0192",
"rw0193",
"rw0194",
"rw0195",
"rw0196",
"rw0197",
"rw0198",
"rw0199",
"rw0200",
"rw0201",
"rw0202",
"rw0203",
"rw0204",
"rw0205",
"rw0206",
"rw0207",
"rw0208",
"rw0209",
"rw0210",
"rw0211",
"rw0212",
"rw0213",
"rw0214",
"rw0215",
"rw0216",
"rw0217",
"rw0218",
"rw0219",
"rw0220",
"rw0221",
"rw0222",
"rw0223",
"rw0224",
"rw0225",
"rw0226",
"rw0227",
"rw0228",
"rw0229",
"rw0230",
"rw0231",
"rw0232",
"rw0233",
"rw0234",
"rw0235",
"rw0236",
"rw0237",
"rw0238",
"rw0239",
"rw0240",
"rw0241",
"rw0242",
"rw0243",
"rw0244",
"rw0245",
"rw0246",
"rw0247",
"rw0248",
"rw0249",
"rw0250",
"rw0251",
"rw0252",
"rw0253",
"rw0254",
"rw0255",
"rw0256",
"rw0257",
"rw0258",
"rw0259",
"rw0260",
"rw0261",
"rw0262",
"rw0263",
"rw0264",
"rw0265",
"rw0266",
"rw0267",
"rw0268",
"rw0269",
"rw0270",
"rw0271",
"rw0272",
"rw0273",
"rw0274",
"rw0275",
"rw0276",
"rw0277",
"rw0278",
"rw0279",
"rw0280",
"rw0281",
"rw0282",
"rw0283",
"rw0284",
"rw0285",
"rw0286",
"rw0287",
"rw0288",
"rw0289",
"rw0290",
"rw0291",
"rw0292",
"rw0293",
"rw0294",
"rw0295",
"rw0296",
"rw0297",
"rw0298",
"rw0299",
"rw0300",
"rw0301",
"rw0302",
"rw0303",
"rw0304",
"rw0305",
"rw0306",
"rw0307",
"rw0308",
"rw0309",
"rw0310",
"rw0311",
"rw0312",
"rw0313",
"rw0314",
"rw0315",
"rw0316",
"rw0317",
"rw0318",
"rw0319",
"rw0320",
"rw0321",
"rw0322",
"rw0323",
"rw0324",
"rw0325",
"rw0326",
"rw0327",
"rw0328",
"rw0329",
"rw0330",
"rw0331",
"rw0332",
"rw0333",
"rw0334",
"rw0335",
"rw0336",
"rw0337",
"rw0338",
"rw0339",
"rw0340",
"rw0341",
"rw0342",
"rw0343",
"rw0344",
"rw0345",
"rw0346",
"rw0347",
"rw0348",
"rw0349",
"rw0350",
"rw0351",
"rw0352",
"rw0353",
"rw0354",
"rw0355",
"rw0356",
"rw0357",
"rw0358",
"rw0359",
"rw0360",
"rw0361",
"rw0362",
"rw0363",
"rw0364",
"rw0365",
"rw0366",
"rw0367",
"rw0368",
"rw0369",
"rw0370",
"rw0371",
"rw0372",
"rw0373",
"rw0374",
"rw0375",
"rw0376",
"rw0377",
]
process.genWeightsTable.namedWeightIDs = named_weights
process.genWeightsTable.namedWeightLabels = named_weights
