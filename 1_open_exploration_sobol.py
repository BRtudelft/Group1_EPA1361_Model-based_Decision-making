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
    policies = pd.read_csv('data/output_data/policies.csv')

    # Perform SOBOl analysis for 1000 scenarios and 100 random policies
    n_scenarios = 1000
    n_policies = 100

    # Run multiprocesser evaluator
    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, results = evaluator.perform_experiments(n_scenarios,
                                                             n_policies,
                                                             uncertainty_sampling=Samplers.SOBOL)

    results_sobol = pd.DataFrame.from_dict(results)
    # outcomes_sobol['policy'] = policies

    # save outcomes to csv file
    experiments.to_csv('data/output_data/experiments_scenario_discovery_1000s100p_sobol.csv')
    results_sobol.to_csv('data/output_data/results_scenario_discovery_1000s100p_sobol.csv')
