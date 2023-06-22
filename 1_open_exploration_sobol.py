""" Open exploration - SOBOL sampling run of the Dike model

The Sobol sampling run of Dike model performed for 1024 scenarios.
Sobol requires the number of samplers to be a power of 2.
A'do nothing' zero policy is implemented, with no active levers.

A multiprocessing evaluator is used and
the outcomes and experiments are saved to the output_data directory
as csv files.

The generated data is analysed in 1_open_exploration.ipynb.

"""

import pandas as pd
import random
from ema_workbench.util import ema_logging
from ema_workbench import (Samplers, Model, MultiprocessingEvaluator,
                           ScalarOutcome, IntegerParameter, optimize,
                           Scenario, Policy
                           )
from problem_formulation import get_model_for_problem_formulation

# make sure pandas is version 1.0 or higher
# make sure networkx is verion 2.4 or higher
print(pd.__version__)
print(nx.__version__)


if __name__ == "__main__":
    random.seed(1361)

    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    n_scenarios = 1024

    # Define 'do nothing' zero policy
    def get_do_nothing_dict():
        return {l.name: 0 for l in model.levers}

    policies = [Policy("policy 0", **dict(get_do_nothing_dict(),**{}),)]

    # Perform model run with Sobol uncertainty sampling
    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, results = evaluator.perform_experiments(
            n_scenarios, policies, uncertainty_sampling=Samplers.SOBOL)

    # Convert results to dataframe
    outcomes_sobol = pd.DataFrame.from_dict(results)

    # Write outcomes and experiments to csv
    experiments.to_csv('data/output_data/OE_sobol_experiments.csv')
    outcomes_sobol.to_csv('data/output_data/OE_sobol_outcomes.csv')
