### Model set-up
# Run with 10000 scenarios, no policies applies
# Can be later on added to the first chapter.
# Imports needed in the model set up are listed below
# NOTE! Model variables must be updated to #scenarios

import pandas as pd
import networkx as nx

# make sure pandas is version 1.0 or higher
# make sure networkx is verion 2.4 or higher
print(pd.__version__)
print(nx.__version__)

from ema_workbench import (
    ema_logging,
    MultiprocessingEvaluator,
    Policy
)
from problem_formulation import get_model_for_problem_formulation

### Problem formulation
if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    # choose problem formulation number, between 0-5
    # each problem formulation has its own list of outcomes
    # we chose #2 because Rijkswaterstaat is interested in highly aggregated outcomes

    dike_model, planning_steps = get_model_for_problem_formulation(2)


    ### Model zero policies

    def get_do_nothing_dict():
        return {l.name: 0 for l in dike_model.levers}


    policies = [
        Policy(
            "policy 0",
            **dict(
                get_do_nothing_dict(),
                **{}
            ),

        )
    ]

    # Assumptions:
    # Scenario's: 20000
    # Policy's: 0 policy and 100 random policies

    scenarios_base = 20000

    # running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_base = evaluator.perform_experiments(scenarios_base, policies)

    # Results of 20000 scenarios and 0 policies saved to csv

    experiments_base, outcomes_base = results_base
    # Policy distinction is necessary because of the legend.
    policies = experiments_base['policy']
    outcomes_20000s_0p = pd.DataFrame.from_dict(outcomes_base)
    outcomes_20000s_0p['policy'] = policies

    # Print outcomes
    outcomes_20000s_0p

    experiments_20000s_0p = experiments_base
    experiments_20000s_0p

    # Both saved to the data map as csv file

    outcomes_20000s_0p.to_csv('data/output_data/outcomes_2000s_0p.csv')
    experiments_20000s_0p.to_csv('data/output_data/experiments_2000s_0p.csv')

    # Number of random policies
    n_random_policies = 100

    # running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_base_random = evaluator.perform_experiments(scenarios_base, n_random_policies)

    # Results of 20000 scenarios and 100 random policies saved to csv
    experiments_base_random, outcomes_base_random = results_base_random

    # Policy distinction is necessary because of the legend.
    policies = experiments_base_random['policy']

    outcomes_20000s_100p_random = pd.DataFrame.from_dict(outcomes_base_random)
    outcomes_20000s_100p_random['policy'] = policies

    experiments_20000s_100p_random = experiments_base_random
    experiments_20000s_100p_random

    outcomes_20000s_100p_random.to_csv('data/output_data/outcomes_20000s_100p_random.csv')
    experiments_20000s_100p_random.to_csv('data/output_data/experiments_20000s_100p_random.csv')


