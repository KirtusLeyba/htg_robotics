import numpy as np

from headlessExperiment import HeadlessPetriDish
from HTGmethods import selectGSCrandLength, selectAll, selectTopN, selectProportional, flatMutate, intMutate
from Task import TaskClump, TaskClumpAtPosition, TaskMaxNeighbors

def run():

    ptA = HeadlessPetriDish(
            size = (400, 300),
            nametag = "A",
            population_size=50,
            robot_data = {
                'max_neighbours' :  5,
                'max_velocity' :    4.0,
                'sense_radius':     50.0,
                'diffuse_rate':     10, 
                'act_rate':         1,
                'nn_info':          {
                                        'hidden_layers' : [],
                                        'activation'    : lambda x : x,
                                            #   RELU:       lambda x : np.maximum(x, 0.0)
                                            #   TANH:       np.tanh
                                            #   LINEAR:     lambda x: x
                                        'modular'       : True,  #TODO: discuss with group why weights should be modular.
                                        'integerWeights' : True
                                    }
                },
            htg_method = lambda x: selectGSCrandLength(x, min_length=2, max_length=4),
            task = TaskMaxNeighbors(min_fitness=0, max_fitness=5),
            fitness_selection_method = lambda x: selectProportional(x),
            mutate_method = lambda x:intMutate(x, 0.1),
            save_interval=10,
            save_filename = "./outputs/headless1.csv",
            max_iters = 10000
            )
    #ptA = PetriDish()
    ptA.run()

if __name__ == "__main__":
    run()
