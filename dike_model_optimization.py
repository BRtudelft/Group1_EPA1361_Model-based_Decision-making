from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
)
from ema_workbench.em_framework.optimization import EpsilonProgress, ArchiveLogger
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    model, steps = get_model_for_problem_formulation(2) #select right problem formulation

#Reference values follow from open exploration - no policy applied here
    reference_values = {
        "Bmax": 175,
        "Brate": 1.5,
        "pfail": 0.5,
        "discount rate 0": 3.5,
        "discount rate 1": 3.5,
        "discount rate 2": 3.5,
        "ID flood wave shape": 4,
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

    espilon = [1e3] * len(model.outcomes) #standard value, afh. van runtime

    nfe = 5000  # Set to number that can be seen as converging


    #toevoegen van archivelogger to caluclate hypervolume _ opnieuw runnen dus!
    convergence_metrics = [
        ArchiveLogger(
            "./archives",  # important to make a new directory archives to save this information
            [l.name for l in model.levers],
            [o.name for o in model.outcomes],
            base_filename="optimization_nfe5000.tar.gz",
        ),
        EpsilonProgress(),
    ]

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
    results.to_csv('data/output_data/results_optimization_5000nfe.csv')
    convergence.to_csv('data/output_data/convergence_optimization_5000nfe.csv')



    #lijkt nu niet nodig?
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True)
    fig, ax1 = plt.subplots(ncols=1)
    ax1.plot(convergence.epsilon_progress)
    ax1.set_xlabel("nr. of generations")
    ax1.set_ylabel(r"$\epsilon$ progress")
    sns.despine()
