# ttH EFT sample generation

This is my attempt at properly generating ttH EFT samples where the Higgs decays to two photons.

## Setup

All necessary ingredients are either included as part of this repository or
available on `/cvmfs`.  Please feel free to use your favorite computing cluster
interactive machine, e.g. [FNAL LPC](https://uscms.org/uscms_at_work/physics/computing/getstarted/uaf.shtml),
[LXplus](https://abpcomputing.web.cern.ch/computing_resources/lxplus/), etc.

To start, please clone this repository in a directory that has sufficient quota for the tutorial (at least 50GB),
```bash
git clone git@github.com:ikrommyd/ttH-EFT-generation.git
```

## Generation

The first section of the tutorial will discuss generating samples of events
with [Madgraph](https://launchpad.net/mg5amcnlo) and
[SMEFTsim](https://smeftsim.github.io/), with weights embedded per-event to
allow reweighting the samples to alternative points in EFT coefficient space.
For this exercise we will generate a $t\bar{t}$ semileptonic sample with one extra jet.

To start, from the main area of this repository, run
```bash
cd ttH-EFT-generation/generation
. setup.sh
```
this sets up the CMS [genproductions](https://github.com/cms-sw/genproductions) git repository
and a local copy of `CMSSW_13_0_14` with additional NanoGEN tools to record EFT weights.

<details>
<summary>Alternative: setup without CMSSW, using LCG</summary>
LCG stack with MG+Pythia+Delphes
</details>

<details>
<summary>Alternative: other UFO models for EFT parameterization</summary>
Alternative generators include SMEFT@NLO, Dim6Top, etc.
  These can be installed using...
</details>

### Creating the gridpack
We will start by creating a gridpack. Start in a fresh terminal window.

Find the files under `genproductions/bin/MadGraph5_aMCatNLO`, Take a look at gridpack_generation.sh. Add a new model SMEFTsim_U35_MwScheme
```bash
export TUTORIALGEN=$(pwd)
cp diagram_generation.sh genproductions/bin/MadGraph5_aMCatNLO/
cd genproductions/bin/MadGraph5_aMCatNLO/
mkdir -pv addons/models/
cd addons/models/
wget https://github.com/SMEFTsim/SMEFTsim/archive/refs/tags/v3.0.2.tar.gz
tar -xvzf v3.0.2.tar.gz
cp -r SMEFTsim-3.0.2/UFO_models/SMEFTsim_U35_MwScheme_UFO .
rm -rf SMEFTsim-3.0.2 v3.0.2.tar.gz
cd SMEFTsim_U35_MwScheme_UFO
```

Create a folder “ttHtoGG_tutorial”
Take a look at ttHtoGG_tutorial_proc_card.dat and ttHtoGG_tutorial_reweight_card.dat
```bash
mkdir ttHtoGG_tutorial
cp $TUTORIALGEN/ttHtoGG* ttHtoGG_tutorial/
```
Let's take a look at some diagrams
```bash
 cd $TUTORIALGEN/genproductions/bin/MadGraph5_aMCatNLO/
 eval `scram unsetenv -sh`
 ./diagram_generation.sh ttHtoGG_tutorial addons/models/SMEFTsim_U35_MwScheme_UFO/ttHtoGG_tutorial/
```

To run locally,
```bash
./gridpack_generation.sh ttHtoGG_tutorial addons/models/SMEFTsim_U35_MwScheme_UFO/ttHtoGG_tutorial
```

<details>
<summary>Alternative: run on condor</summary>
Condor gridpack generation works for lxplus (and LPC?) but may not work at your local cluster, depending on your cluster's batch setup. You could use CMS connect as well (link)

```bash
nohup ./submit_cmsconnect_gridpack_generation.sh ttHtoGG_tutorial addons/cards/SMEFTsim_U35_MwScheme_UFO/ttHtoGG_tutorial > ttHtoGG_tutorial.log
```
</details>

### Generating NanoGEN files

NanoGEN is a very convenient format for exploratory studies.
The event content of the flat trees is similar to the generator infomration in NanoAOD,
but much faster generation time because the detector simulation and reconstruction is being skipped.

We will generate a few events directly from the gridpack created in the previous step (no intermediate GEN file is needed!), and use the same pythia fragment as in the GEN step before.
Make sure you are in `ttH-EFT-generation2023/generation/` and have a CMSSW environment set (e.g. run `. setup.sh` again to be sure).

A cmsRun config file can be created

``` bash
cmsDriver.py Configuration/GenProduction/python/pythia_fragment.py \
    --python_filename nanogen_cfg.py --eventcontent NANOAODGEN \
    --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD \
    --customise_commands "process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=123" \
    --fileout file:nanogen_123.root --conditions 130X_mcRun3_2023_realistic_v14 --beamspot Realistic25ns13p6TeVEarly2023Collision \
    --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run3 --no_exec --mc -n 100

```

The CMSSW area that has been set up in the previous step already includes a useful tool that extracts the coefficients of the polynomial fit.
You'll learn more about the coefficients and how to use them in a later part.
Documentation of the used package can be found on the [mgprod github repo](https://github.com/TopEFT/mgprod#additional-notes-on-the-production-of-naod-samples).
If we want to keep the original weights we can add them to the list of named weights in the NanoGEN config file:

``` bash
echo "named_weights = [" >> nanogen_cfg.py
cat ttHtoGG_tutorial_reweight_card.dat | grep launch | sed 's/launch --rwgt_name=/"/' | sed 's/$/",/' >> nanogen_cfg.py
echo -e "]\nprocess.genWeightsTable.namedWeightIDs = named_weights\nprocess.genWeightsTable.namedWeightLabels = named_weights" >> nanogen_cfg.py
```

Producing NanoGEN is fairly fast, and a few thousand events can usually be produced locally like

``` bash
cmsRun nanogen_cfg.py
```

#### Checking the weights

It is always a good idea to check if some of the weights have enhanced tails.
A simple script that reads the weights and makes a histogram for the pure `ctG` contributions can be run with

``` bash
. setup_hist.sh
python weights.py
```

Additionally, it is always a good idea to compare a reweighted sample with a sample that has been produced at a fixed EFT point.

``` bash
python closure.py
```
