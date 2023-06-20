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
random.seed(1361)


if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2) #select right problem formulation

#Reference values follow from open exploration - based on assumption of worst case scenario
    reference_values = {
        "Bmax": 182.32, #Per dijkring - breach width
        "Brate": 4.16, #Per dijkring -how fast breach grows over time
        "pfail": 0.36, #Per dijkring - Kans dat dijk niet breekt
        "discount rate 0": 2.87, #Calculating present rate values - time step 1
        "discount rate 1": 2.84, #Calculating present rate values - time step 2
        "discount rate 2": 2.86, #Calculating present rate values - time step 3
        "ID flood wave shape": 84, #Welke flood wave shape wordt gebruikt
    }
    scen1 = {}

    for key in model.uncertainties:
        name_split = key.name.split("_")

        if len(name_split) == 1:
            scen1.update({key.name: reference_values[key.name]})

        else:
            scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario("reference", **scen1)

    convergence_metrics = [EpsilonProgress()]

    espilon = [1e3] * len(model.outcomes)

    nfe = 10000

    #Perform model evaluation
    with MultiprocessingEvaluator(model) as evaluator:
        #wat te doen met losse convergence file?
        results, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=espilon,
            convergence=convergence_metrics,
            reference=ref_scenario, #reference scenario is defined
        )

    #save outcomes to csv file
    results.to_csv('data/output_data_oud_check/results_optimization_10000nfe.csv')
    convergence.to_csv('data/output_data_oud_check/convergence_optimization_10000nfe.csv')