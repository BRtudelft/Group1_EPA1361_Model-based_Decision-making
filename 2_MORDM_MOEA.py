from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
)
from ema_workbench.em_framework.optimization import EpsilonProgress, HyperVolume
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns
import random

##Intro van inhoud file - beargumentatie hoeveel nfe enzo?

if __name__ == "__main__":
    random.seed(1361)

    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2)

    # Reference values follow from open exploration
    reference_values = {
        "A.1_Bmax": 107.338439,
        "A.1_Brate": 1.5,
        "A.1_pfail": 0.327612,
        "A.2_Bmax": 36.22951,
        "A.2_Brate": 1.0,
        "A.2_pfail": 0.067184,
        "A.3_Bmax": 203.73302,
        "A.3_Brate": 1.5,
        "A.3_pfail": 0.099837,
        "A.4_Bmax": 36.591975,
        "A.4_Brate": 10,
        "A.4_pfail": 0.957634,
        "A.5_Bmax": 179.7911,
        "A.5_Brate": 10,
        "A.5_pfail": 0.017638,
        "discount rate 0": 4.5,
        "discount rate 1": 3.5,
        "discount rate 2": 1.5,
        "A.0_ID flood wave shape": 104,
    }

    ref_scenario = Scenario("reference", **reference_values)

    convergence_metrics = [EpsilonProgress()]

    epsilon = [1e3] * len(model.outcomes)

    nfe = 10000

    # Perform model evaluation
    with MultiprocessingEvaluator(model) as evaluator:
        results, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=epsilon,
            convergence=convergence_metrics,
            reference=ref_scenario, #reference scenario is defined
        )

    # Save outcomes to csv file
    results.to_csv('data/output_data/MOEA_results_10000nfe.csv')
    convergence.to_csv('data/output_data/MOEA_convergence_10000nfe.csv')