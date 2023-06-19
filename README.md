### EPA1361 Model-based Decision-making

Welcome to model made by group 1: Friso Pladet, Finn Blom, Suze van Santen, Mart Vloet, Max Kerpel, Kas Hogeboom & Britt Reddingius

### Contents
- [MORDM_0_model_setup.py] 
  _This code shows the setup of the model_
- [MORDM_1_problem_formulation.ipynb]
  _This is the problem formulated in the model_
- [MORDM_2_generating_alternatives.ipynb] 
  __
- [MORDM_3_uncertainty_analysis.ipynb] 
  __
- [MORDM_4_scenario_discovery_&_trade-off.ipynb] 
  __

  
### Requirements
## ema_workbench
This repository is tested on Python 3.11. It has the same dependencies as the EMAworkbench version 2.4.1 
(see [installation guide] (https://emaworkbench.readthedocs.io/en/latest/getting_started/installation.html)). 
Furthermore, it uses [seaborn](https://github.com/mwaskom/seaborn) for many of the plots.
Make sure that you have installed ema_workbench by creator quaquel.
```
pip install -U ema_workbench[recommended] seaborn
```

## Imports
All the imports needed to run this model are listed below, 
please check if all of these are functional before running the model. 
`
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
`

## Versions
Make sure pandas is version 1.0 or higher and networkx is version 2.4 or higher by running the following command:

_print(pd.__version__)
print(nx.__version__)_