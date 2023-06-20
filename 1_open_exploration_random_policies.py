# Open exploration

### Model set-up: random 100 policies
# Run with 1.000 scenarios, 100 random policies applied.

import pandas as pd
import networkx as nx
import random
from ema_workbench import (
    ema_logging,
    MultiprocessingEvaluator,
    Policy)
from problem_formulation import get_model_for_problem_formulation

# make sure pandas is version 1.0 or higher
# make sure networkx is verion 2.4 or higher
print(pd.__version__)
print(nx.__version__)

random.seed(1361)

### Problem formulation
if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    dike_model, planning_steps = get_model_for_problem_formulation(2)

    n_scenarios = 1000
    n_random_policies = 100

    # running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_random = evaluator.perform_experiments(n_scenarios, n_random_policies)

    experiments_random, outcomes_random = results_random
    # Select policies from experiments dataframe
    policies = experiments_random['policy']

    # Create Dataframe for outcomes
    outcomes_random = pd.DataFrame.from_dict(outcomes_random)
    # Add policy column
    outcomes_random['policy'] = policies

    # Both outcomes and experiments saved to the data map as csv file
    outcomes_random.to_csv('data/output_data/OE_outcomes_random.csv')
    experiments_random.to_csv('data/output_data/OE_experiments_random.csv')

