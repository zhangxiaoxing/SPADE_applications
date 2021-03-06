# SPADE_applications
---
Repository containing code necessary to reproduce the results of 
Stella, A., Quaglio, P., Torre, E., & Grün, S. (2019). 3d-SPADE: Significance Evaluation of Spatio-Temporal Patterns of Various Temporal Extents. _Biosystems_.
[Link to the paper](https://doi.org/10.1016/j.biosystems.2019.104022)

## Installation
```sh
$ git clone git@github.com:INM-6/SPADE_applications.git
```

## Concept
The Spike PAttern Detection and Evaluation (SPADE) method is able to find and statistically evaluate spatio-temporal patterns in parallel spike train data. In the paper, we introduce an extention to the testing procedure of SPADE, so that it accounts statistically to the temporal duration of the pattern. This modification improves the statistical performance of SPADE, while essentially maintaining intact its computational performance. We show that a) the statistical performance is improved for the case of synthetic datasets involving patterns of multiple extents (Figure 3), b) the statistical performance is unchanged if all patterns have the same temporal duration (Figure 4), and c) the computational performance is unchanged, for different parameter settings (Figure 6).
The code present here makes possible the reproduction of all three figures.
Finally, for all three cases, for the generation of the artificial data, its analysis and the generation of the figures of the manuscript, we used the workflow management system [Snakemake](https://snakemake.readthedocs.io). Figure 7 of the paper represents the Snakemake workflow we designed to obtain Figure 3.


## Dependencies
To run the analysis presented in the paper, we created a virtual environment file (envs/SPADE_applications.yml) that installs all packages needed to reproduce our results. In order to do so, you need [Conda](https://www.anaconda.com/distribution/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
```sh
$ cd envs
$ conda env create -f SPADE_applications.yml
$ source activate SPADE_applications
```
In the SPADE_applications environment, an essential package needed is [elephant](https://elephant.readthedocs.io/en/latest/index.html). 
**Elephant** is "an emerging open-source, community centered library for the analysis of electrophysiological data in the Python programming language. The focus of Elephant is on generic analysis functions for spike train data and time series recordings from electrodes, such as the local field potentials (LFP) or intracellular voltages. "
SPADE is part of elephant, and for any additional documentation for the usage of the method, we refer to [here](https://elephant.readthedocs.io/en/latest/reference/spade.html).

## Usage
The repository is structured in three folders:
* `multiple_pattern durations`: contains the code necessary to reproduce Figure 3
* `validation_FPFN`: contains the code necessary to reproduce Figure 4
* `profiling`: contains the code necessary to reproduce Figure 6

To run the code:
```sh
$ cd folder/code
$ source activate SPADE_applications
$ ./snakejob.sh
```
We suggest to run the `validation_FPFN` workflow on a cluster, since many (4 x 8 x 8 x 100) datasets are generated and the SPADE method is run on each dataset, making the job computationally and memory intensive.

---
## Acknowledgements
Funding was received from European Union’s Horizon 2020 Framework Programme for Research and Innovation under Spe-
cific Grant Agreement No. 785907 (Human Brain Project SGA2), Deutsche Forschungsgemeinschaft Grants GR 1753/4-2 and DE 2175/2-1 of the Priority Program (SPP 1665) and RTG2416 MultiSenses-MultiScales.



