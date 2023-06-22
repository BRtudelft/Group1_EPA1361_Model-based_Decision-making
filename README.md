# EPA1361 Model-based Decision-making - GROUP 1
This repository presents analysis performed by Group 1 on the dike_model for the course EPA1361 Model-based Decision-making at TU Delft.
The original model was provided by course instructors and is based on the Room for the River IJssel case. 

Group 1:
Friso Pladet, Finn Blom, Suze van Santen, Mart Vloet, Max Kerpel, Kas Hogeboom 
& Britt Reddingius

### The model is used to select potential policies that could be implemented in the flood prevention of the IJssel river in the Netherlands. 

Within the repository, you will find three distinct files dedicated to open exploration. This division exists because 
two Python files (.py) were utilized for generating data, while the Notebook files (.ipynb) were employed for data 
visualization. Notebooks excel at visualization but lack the necessary speed for handling numerous iterations promptly. 

## Contents
The py files are generating data and the ipynb notebooks are interpreting the data. The numbers 1 through 4 distinguish
the different steps and datafiles used in the model.

- [1_open_exploration.ipynb](1_open_exploration.ipynb)
  - Open exploration of the dike model
- [1_open_exploration_random_policies.py](1_open_exploration_random_policies.py)
  - Generated data is analysed in [1_open_exploration.ipynb](1_open_exploration.ipynb)
- [1_open_exploration_sobol.py](1_open_exploration_sobol.py)
  - Generated data is analysed in [1_open_exploration.ipynb](1_open_exploration.ipynb)
- [1_open_exploration_zero_policy.py](1_open_exploration_zero_policy.py)
  - Generated data is analysed in [1_open_exploration.ipynb](1_open_exploration.ipynb)
- [2_DS_MORDM_generating_alternatives.ipynb](2_DS_MORDM_generating_alternatives.ipynb)
  - Analysis of generated policy proposals
- [2_MORDM_MOEA.py](2_MORDM_MOEA.py)
  - Implementation of MOEA. Generated data is analysed in [2_DS_MORDM_generating_alternatives.ipynb](2_DS_MORDM_generating_alternatives.ipynb)
- [3_DS_MORDM_uncertainty_analysis.ipynb](3_DS_MORDM_uncertainty_analysis.ipynb)
  - Uncertainty analysis of selected policy proposals
- [3_MORDM_uncertainty.py](3_MORDM_uncertainty.py)
  - Generated data is analysed in [3_DS_MORDM_uncertainty_analysis.ipynb](3_DS_MORDM_uncertainty_analysis.ipynb)
- [4_DS_MORDM_scenario_discovery.ipynb](4_DS_MORDM_scenario_discovery.ipynb)
  - Scenario discovery of selected policy proposals

### Input functions from EPA1361 course
- [dike_model_function.py](dike_model_function.py)
- [dike_model_simulation.py](dike_model_simulation.py)
- [funs_dikes.py](funs_dikes.py)
- [funs_economy.py](funs_economy.py)
- [funs_generate_network.py](funs_generate_network.py)
- [funs_hydrostat.py](funs_hydrostat.py)
- [problem_formulation.py](problem_formulation.py)

## Requirements
### ema_workbench
This repository is tested on Python 3.11. It has the same dependencies as the EMAworkbench version 2.4.1 
(see [installation guide] (https://emaworkbench.readthedocs.io/en/latest/getting_started/installation.html)). 
Furthermore, it uses [seaborn](https://github.com/mwaskom/seaborn) for many of the plots.
Make sure that you have installed ema_workbench by creator quaquel.
```
pip install -U ema_workbench[recommended] seaborn
```

For optimization, the ema_workbench relies on a library called platypus-opt. platypus-opt is python package developed 
by David Hadka (http://platypus.readthedocs.io/en/latest/) for multi-objective optimization. 
you can use pip to install it:
```
pip install platypus-opt
```

## Imports
All the imports needed to run this model are listed below, 
please check if all of these are functional before running the model. 
```
import copy
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
import scipy as sp
import seaborn as sns
import time

from collections import defaultdict

from ema_workbench.analysis import (feature_scoring, 
                                    prim, 
                                    dimensional_stacking, 
                                    parcoords)

from ema_workbench import (Model,
                           RealParameter, 
                           ScalarOutcome,
                           MultiprocessingEvaluator, 
                           ema_logging,
                           Constant, 
                           SequentialEvaluator, 
                           Policy, 
                           Scenario,
                           IntegerParameter, 
                           CategoricalParameter,
                           IntegerParameter, 
                           ArrayOutcome,
                           optimize)

from ema_workbench.em_framework.evaluators import perform_experiments

from ema_workbench.em_framework.samplers import sample_uncertainties

from ema_workbench.util import ema_logging

from ema_workbench.em_framework import get_SALib_problem
from SALib.analyze.sobol import analyze
from SALib.analyze import sobol_
```
## Versions
Make sure pandas is version 1.0 or higher and networkx is version 2.4 or higher by running the following command:

```
print(pd.__version__)
print(nx.__version__)
```