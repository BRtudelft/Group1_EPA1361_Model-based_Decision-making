# Open exploration

### Model set-up: zero policy
# Run with 20.000 scenarios, zerorandom policies applied.

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

    def get_do_nothing_dict():
        return {l.name: 0 for l in dike_model.levers}

    policies = [
        Policy(
            "policy zero",
            **dict(
                get_do_nothing_dict(),
                **{}
            ),
        )
    ]

    n_scenarios = 20000

    # Running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_zero = evaluator.perform_experiments(n_scenarios, policies)

    experiments_zero, outcomes_zero = results_zero
    # Select policies from experiments dataframe
    policies = experiments_zero['policy']

    # Create Dataframe for outcomes
    outcomes_zero = pd.DataFrame.from_dict(outcomes_zero)
    # Add policy column
    outcomes_zero['policy'] = policies

    # Both outcomes and experiments saved to the data map as csv file
    outcomes_zero.to_csv('data/output_data/OE_outcomes_zero.csv')
    experiments_zero.to_csv('data/output_data/OE_experiments_zero.csv')

