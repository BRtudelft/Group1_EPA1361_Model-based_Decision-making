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


if __name__ == "__main__":
    random.seed(1361) #Seed verplaatst

    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2) #select right problem formulation

    #policies includes an unnamed column with index from original dataframe with solutions
    selected_policies = pd.read_csv('data/output_data/MOEA_selected_policies.csv')
    #    selected_policies.drop(['policy'])

    #Check with minimal number of scenarios, total of 5 policies - 10000 scenarios
    n_scenarios = 10000

    policies_to_evaluate = []
    for i, policy in selected_policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))
    print(policies_to_evaluate)

    with MultiprocessingEvaluator(model) as evaluator:
        results_uncertainty = evaluator.perform_experiments(n_scenarios, policies_to_evaluate)

    experiments, outcomes = results_uncertainty
    # Policy distinction is necessary because of the legend.
    policies = experiments['policy']

    outcomes_uncertainties = pd.DataFrame.from_dict(outcomes)
    outcomes_uncertainties['policy'] = policies

    #save outcomes to csv file
    experiments.to_csv('data/output_data/MOEA_uncertainty_experiments.csv')
    outcomes_uncertainties.to_csv('data/output_data/MOEA_uncertainty_outcomes.csv')