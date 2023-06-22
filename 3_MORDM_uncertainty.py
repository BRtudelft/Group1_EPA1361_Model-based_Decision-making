""" MORDM framework - Uncertainty run

The five policies selected in 2_DS_MORDM_generating_alternatives.ipynb
are evaluated over 10.000 different random scenarios.

A multiprocessing evaluator is used and the outcomes and
experiments are saved to the output_data directory as csv files.

The generated data is analysed in 3_DS_MORDM_uncertainty_analysis.ipynb

"""

import pandas as pd
import networkx as nx
from ema_workbench.util import ema_logging
from ema_workbench import (MultiprocessingEvaluator, Policy)
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

    n_scenarios = 10000

    selected_policies = pd.read_csv('data/output_data/MOEA_selected_policies.csv')

    policies_to_evaluate = []
    for i, policy in selected_policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))


    with MultiprocessingEvaluator(model) as evaluator:
        results_uncertainty = evaluator.perform_experiments(n_scenarios, policies_to_evaluate)

    experiments, outcomes = results_uncertainty

    # Select policies from experiments dataframe
    policies = experiments['policy']

    # Convert outcomes to dataframe
    outcomes_uncertainties = pd.DataFrame.from_dict(outcomes)
    # Add policy column to outcomes dataframe
    outcomes_uncertainties['policy'] = policies

    # Write outcomes and experiments to csv
    experiments.to_csv('data/output_data/MOEA_uncertainty_experiments.csv')
    outcomes_uncertainties.to_csv('data/output_data/MOEA_uncertainty_outcomes.csv')