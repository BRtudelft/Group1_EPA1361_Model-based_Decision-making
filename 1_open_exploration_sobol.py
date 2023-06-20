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

# Note that the Sobol analysis will require N(2k+2) samples, where N is a baseline number of experiments
# required to cover the uncertainties (let's also assume 1000 in this case) and k is the number of uncertainties.
#The balance properties of Sobol' points require n to be a power of 2

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    # Perform SOBOl analysis for 1024 scenarios 2^10
    n_scenarios = 1024


    def get_do_nothing_dict():
        return {l.name: 0 for l in model.levers}


    policies = [
        Policy(
            "policy 0",
            **dict(
                get_do_nothing_dict(),
                **{}
            ),
        )
    ]

## ZOALS BESCHREVEN IN ASSIGNMENT 6
    # Run multiprocesser evaluator
    with MultiprocessingEvaluator(model, n_processes=-1) as evaluator:
        experiments, results = evaluator.perform_experiments(n_scenarios,
                                                             policies,
                                                             uncertainty_sampling=Samplers.SOBOL)

    results_sobol = pd.DataFrame.from_dict(results)
    # outcomes_sobol['policy'] = policies

    # save outcomes to csv file
    experiments.to_csv('data/output_data/sobol_open_exploration_1000s_experiments.csv')
    results_sobol.to_csv('data/output_data/sobol_open_exploration_1000s_results.csv')
