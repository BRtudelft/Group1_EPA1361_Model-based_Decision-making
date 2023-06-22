""" Open exploration - Run of Dike model without policies

The Dike model is run with problem formulation 2 for 20.000 random
scenarios. A 'do nothing' zero policy is implemented, with no
active levers.

A multiprocessing evaluator is used and the outcomes and
experiments are saved to the output_data directory as csv files.

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

    n_scenarios = 20000

    # Define 'do nothing' zero policy
    def get_do_nothing_dict():
        return {l.name: 0 for l in dike_model.levers}


    policies = [Policy("policy 0", **dict(get_do_nothing_dict(), **{}), )]

    # Perform model run with multiprocessing evaluator
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_zero = evaluator.perform_experiments(n_scenarios, policies)

    experiments_zero, outcomes_zero = results_zero

    # Select policies from experiments dataframe
    policies = experiments_zero['policy']

    # Convert outcomes_zero to dataframe
    outcomes_zero = pd.DataFrame.from_dict(outcomes_zero)
    # Add policy column to outcomes dataframe
    outcomes_zero['policy'] = policies

    # Write outcomes and experiments to csv
    outcomes_zero.to_csv('data/output_data/OE_outcomes_zero.csv')
    experiments_zero.to_csv('data/output_data/OE_experiments_zero.csv')

