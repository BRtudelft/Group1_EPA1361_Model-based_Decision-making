### Model set-up
# Two runs has been executed for the open exploration:
# Run with 1000 scenarios, no policies applied.
# Run with 1000 scenarios, 100 random policies applied

# NOTE! Model variables must be updated to #scenarios

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

    # choose problem formulation number, between 0-5
    # each problem formulation has its own list of outcomes
    # we chose #2 because Rijkswaterstaat is interested in highly aggregated outcomes

    dike_model, planning_steps = get_model_for_problem_formulation(2)

    #Run 1: Model zero policies
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
    # Scenario's: 1000
    # Policy's: 0 policy

    scenarios_base = 1000

    # Running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_base = evaluator.perform_experiments(scenarios_base, policies)

    experiments_base, outcomes_base = results_base
    # Policy distinction is necessary because of the legend.
    policies = experiments_base['policy']

    # Create Dataframe for outcomes & add policy column
    outcomes_20000s_0p = pd.DataFrame.from_dict(outcomes_base)
    outcomes_20000s_0p['policy'] = policies

    experiments_20000s_0p = experiments_base

    # Both outcomes and experiments saved to the data map as csv file
    outcomes_20000s_0p.to_csv('data/output_data/outcomes_20000s_0p.csv')
    experiments_20000s_0p.to_csv('data/output_data/experiments_20000s_0p.csv')

    # Run 2: Model 100 random policies

    # Assumptions:
    # Scenario's: 1000
    # Policy's: 100 policy

    n_random_policies = 100

    # running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_base_random = evaluator.perform_experiments(scenarios_base, n_random_policies)

    experiments_base_random, outcomes_base_random = results_base_random
    # Policy distinction is necessary because of the legend.
    policies = experiments_base_random['policy']

    # Create Dataframe for outcomes & add policy column
    outcomes_20000s_100p_random = pd.DataFrame.from_dict(outcomes_base_random)
    outcomes_20000s_100p_random['policy'] = policies

    experiments_20000s_100p_random = experiments_base_random

    # Both outcomes and experiments saved to the data map as csv file
    outcomes_20000s_100p_random.to_csv('data/output_data/outcomes_20000s_100p_random.csv')
    experiments_20000s_100p_random.to_csv('data/output_data/experiments_20000s_100p_random.csv')

    # # Merge datasets
    # outcomes_0 = pd.read_csv('data/output_data/outcomes_20000s_0p.csv')
    # outcomes_random = pd.read_csv('data/output_data/outcomes_20000s_100p_random.csv')
    # outcomes_complete = outcomes_0.merge(outcomes_random, how='outer')
    #
    # experiments_0 = pd.read_csv('data/output_data/experiments_20000s_0p.csv')
    # experiments_random = pd.read_csv('data/output_data/experiments_20000s_100p_random.csv')
    # experiments_complete = experiments_0.merge(experiments_random, how='outer')
    #
    # # Check how this looks by printing
    # outcomes_complete
    # experiments_complete

