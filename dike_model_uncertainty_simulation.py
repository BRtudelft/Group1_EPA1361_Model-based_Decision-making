import pandas as pd
from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
    Policy
)

from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation

import random

# Select seed
random.seed(1361)

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2) #select right problem formulation

    #policies includes an unnamed column with index from original dataframe with solutions
    policies = pd.read_csv('data/output_data/policies.csv')

    n_scenarios = 5000ç

    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))
    print(policies_to_evaluate)

    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        results = evaluator.perform_experiments(n_scenarios, policies_to_evaluate)

    experiments, outcomes = results
    # Policy distinction is necessary because of the legend.
    policies = experiments['policy']

    outcomes_uncertainties = pd.DataFrame.from_dict(outcomes)
    outcomes_uncertainties['policy'] = policies

    #save outcomes to csv file
    experiments.to_csv('data/output_data/experiments_uncertainty_simulation_5000s.csv')
    outcomes_uncertainties.to_csv('data/output_data/outcomes_uncertainty_simulation_5000s.csv')