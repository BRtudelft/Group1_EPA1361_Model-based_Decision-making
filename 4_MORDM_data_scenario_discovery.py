import random
import pandas as pd
from problem_formulation import get_model_for_problem_formulation
from ema_workbench.util import ema_logging
from ema_workbench import (
    Samplers,
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
    Policy
)

# Select seed
random.seed(1361)

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    # Policies includes an unnamed column with index from original dataframe with solutions
    policies = pd.read_csv('data/output_data_oud_check!/policies.csv')

    # We run 10 to test if it saves correctly
    n_scenarios = 10

    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))
        print(i)

    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, results = evaluator.perform_experiments(n_scenarios,
                                                             policies_to_evaluate,
                                                             uncertainty_sampling=Samplers.SOBOL)

    results_sobol = pd.DataFrame.from_dict(results)
    # outcomes_sobol['policy'] = policies

    # save outcomes to csv file
    experiments.to_csv('data/output_data_oud_check!/experiments_scenario_discovery_10s_sobol.csv')
    results_sobol.to_csv('data/output_data_oud_check!/results_scenario_discovery_10s_sobol.csv')

