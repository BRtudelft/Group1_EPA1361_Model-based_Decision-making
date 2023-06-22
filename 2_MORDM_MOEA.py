""" MORDM framework - MOEA application

The MOEA is used to find pareto optimal combinations of levers for which
the outcomes are minimized. The ema_workbench relies on the platypus-opt
package for this optimization. A reference scenario is based on the
combination of uncertainty parameters for which the model under
the 'do nothing' zero policy presents the maximum number of deaths and
expected annual damages.

The MOEA is run with 10.000 NFE and the results and convergence data are
saved to the output_data directory as csv files.

The generated data is analysed in 2_DS_MORDM_generating_alternatives.ipynb.

"""

import pandas as pd
import networkx as nx
from ema_workbench.util import ema_logging
from ema_workbench.em_framework.optimization import EpsilonProgress
from ema_workbench import (MultiprocessingEvaluator, Scenario)
from problem_formulation import get_model_for_problem_formulation
import random

# Make sure pandas is version 1.0 or higher
# Make sure networkx is verion 2.4 or higher
print(pd.__version__)
print(nx.__version__)


if __name__ == "__main__":
    random.seed(1361)

    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    # Define reference values of uncertainty analysis
    reference_values = {
        "A.1_Bmax": 107.338439,
        "A.1_Brate": 1.5,
        "A.1_pfail": 0.327612,
        "A.2_Bmax": 36.22951,
        "A.2_Brate": 1.0,
        "A.2_pfail": 0.067184,
        "A.3_Bmax": 203.73302,
        "A.3_Brate": 1.5,
        "A.3_pfail": 0.099837,
        "A.4_Bmax": 36.591975,
        "A.4_Brate": 10,
        "A.4_pfail": 0.957634,
        "A.5_Bmax": 179.7911,
        "A.5_Brate": 10,
        "A.5_pfail": 0.017638,
        "discount rate 0": 4.5,
        "discount rate 1": 3.5,
        "discount rate 2": 1.5,
        "A.0_ID flood wave shape": 104,
    }

    ref_scenario = Scenario("reference", **reference_values)

    convergence_metrics = [EpsilonProgress()]

    epsilon = [1e3] * len(model.outcomes)

    nfe = 10000

    # Perform model evaluation
    with MultiprocessingEvaluator(model) as evaluator:
        results, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=epsilon,
            convergence=convergence_metrics,
            reference=ref_scenario,
        )

    # Write results and convergence to csv
    results.to_csv('data/output_data/MOEA_results_10000nfe.csv')
    convergence.to_csv('data/output_data/MOEA_convergence_10000nfe.csv')