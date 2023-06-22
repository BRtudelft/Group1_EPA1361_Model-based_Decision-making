"""Open exploration - Run of the Dike model with 100 random policies

The Dike model is run with problem formulation 2 for 1000 scenarios
and 100 random policies. A multiprocessing evaluator is used and
the outcomes and experiments are saved to the output_data directory
as csv files.

The generated data is analysed in 1_open_exploration.ipynb.

"""

import pandas as pd
import networkx as nx
import random
from ema_workbench import (ema_logging, MultiprocessingEvaluator,
                           Policy
                           )
from problem_formulation import get_model_for_problem_formulation

# Make sure pandas is version 1.0 or higher
# Make sure networkx is verion 2.4 or higher
print(pd.__version__)
print(nx.__version__)


if __name__ == "__main__":
    random.seed(1361)

    ema_logging.log_to_stderr(ema_logging.INFO)

    dike_model, planning_steps = get_model_for_problem_formulation(2)

    n_scenarios = 1000
    n_random_policies = 100

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_random = evaluator.perform_experiments(n_scenarios,
                                                       n_random_policies)

    experiments_random, outcomes_random = results_random

    # Select policy column from experiments dataframe
    policies = experiments_random['policy']

    # Convert outcomes_random to dataframe
    outcomes_random = pd.DataFrame.from_dict(outcomes_random)
    # Add policy column to outcomes dataframe
    outcomes_random['policy'] = policies

    # Write outcomes and experiments to csv
    outcomes_random.to_csv('data/output_data/OE_outcomes_random.csv')
    experiments_random.to_csv('data/output_data/OE_experiments_random.csv')


