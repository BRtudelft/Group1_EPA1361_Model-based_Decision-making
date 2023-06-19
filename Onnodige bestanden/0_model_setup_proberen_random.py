import pandas as pd
import networkx as nx
import numpy as np
import random

# Make sure pandas is version 1.0 or higher
# Make sure networkx is version 2.4 or higher
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

    # Choose problem formulation number, between 0-5
    # Each problem formulation has its own list of outcomes
    # We chose #2 because Rijkswaterstaat is interested in highly aggregated outcomes
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

    # Running the model through EMA workbench
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_base = evaluator.perform_experiments(scenarios_base, policies)

    # Results of 20000 scenarios and 0 policies saved to CSV
    experiments_base, outcomes_base = results_base

    # Policy distinction is necessary because of the legend.
    policies = experiments_base['policy']
    outcomes_2000s_0p = pd.DataFrame.from_dict(outcomes_base)
    outcomes_2000s_0p['policy'] = policies

    # Print outcomes
    outcomes_2000s_0p

    experiments_2000s_0p = experiments_base

    # Both saved to the data map as CSV files
    outcomes_2000s_0p.to_csv('data/output_data/outcomes_2000s_0p.csv')
    experiments_2000s_0p.to_csv('data/output_data/experiments_2000s_0p.csv')

    ### Model random policies

    # Define the number of random scenarios
    scenarios_random = 100

    # Generate random values for each uncertainty variable
    uncertainties_random = {
        uncertainty.name: np.random.uniform(uncertainty.lower_bound, uncertainty.upper_bound, scenarios_random)
        for uncertainty in dike_model.uncertainties
    }

    # Create a list of random policies
    policies_random = []
    for i in range(scenarios_random):
        policy_name = f"Random Policy {i + 1}"
        policy_values = {
            lever.name: random.choice([0, 1])  # Assuming binary levers (0: no action, 1: action)
            for lever in dike_model.levers
        }
        policies_random.append(Policy(policy_name, **policy_values))

    # Combine the "do-nothing" policy with the random policies
    policies_combined = [Policy("Policy 0", **get_do_nothing_dict())] + policies_random

    # Run the model with the combined policies and scenarios
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results_combined = evaluator.perform_experiments(scenarios_random + 1, policies_combined)

    # Extract and save the results for the random scenarios
