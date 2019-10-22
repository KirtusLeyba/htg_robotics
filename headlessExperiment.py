from HTGmanager import HtgManager
from HTGmethods import selectGSCrandLength, selectAll, flatMutate
from Task import TaskClump
from DataMethods import DataRecorder
import numpy as np

class HeadlessPetriDish:

    def __init__(self,
            size = (400, 300),
            nametag = "A",
            population_size=50,
            robot_data = {
                'max_neighbours' :  5,
                'max_velocity' :    4.0,
                'sense_radius':     50.0,
                'diffuse_rate':     10, # TODO convert from timesteps to secs.
                'act_rate':         1, # TODO convert from timesteps to secs.
                'nn_info':          {
                                        'hidden_layers' : [],
                                        'activation'    : lambda x : x,
                                        'modular'       : True
                                    }
                },
            htg_method=lambda x: selectGSCrandLength(x, min_length=2, max_length=4),
            task=TaskClump(0, 100),
            fitness_selection_method=selectAll,
            mutate_method = lambda x: flatMutate(x, 0.1),
            visuals = {
                'colour_A'      : [100.0, 100.0, 100.0],
                'colour_B'      : [0.0, 225.0, 0.0],
                'background'    : [250.0, 220.0, 180.0],
                'draw_radius'   : False,
                'draw_transfer' : True
                },
            save_interval=-1,
            record_interval = 10,
            max_iters = 1000,
            save_filename = 'outputs/' + 'headless_run.csv',
            ):
        """
        size                -- dimension of the screen: (float, float) (default: (400, 300))
        nametag             -- name of the experiment: string (default: "A")
        population_size     -- number of individuals: int (default: 50)
        robot_data          -- dict. of robot params: dictionary (default:
                    {
                        'max_neighbours' :  5,      -- max. number of neighbours a robot can see.
                        'max_velocity' :    4.0,    -- max. velocity a robot can reach.
                        'sense_radius':     50.0,   -- radius of sensory detection.
                        'diffuse_rate':     10,     -- ticks per gene diffusion.
                        'act_rate':         1,      -- ticks per robot action.
                        nn_info : dict
                            default: {
                                'hidden_layers' : [],                   -- number of hidden layers (input and output are defined by default).
                                'activation'    : lambda x : x,         -- activation function (e.g. np.tanh, ReLU, or just linear).
                                'modular'       : True                  -- whether the weights are the same for each robots sensor channel.
                            }
                                                        are the same. Generally, this makes sense to
                                                        keep true.
                    })
        htg_method          -- method describing how genes are selected.
        visuals             -- colours of graphics: dictionary (default:
                    {
                        'colour_A'          : [100.0, 100.0, 100.0],    -- colour when there are no neighbours.
                        'colour_B'          : [0.0, 225.0, 0.0],        -- colour when there are max. neighbours.
                        'background'        : [250.0, 220.0, 180.0]     -- colour of background.
                        'draw_radius'       : False                     -- whether to draw the visual radius of a robot.
                        'draw_transfer'     : True                      -- whether to draw the gene transfer lines.
                    })
        save_interval       -- how often (in frames) should the data of the population be saved. -1 means never: int (default: -1)
        record_interval     -- how ofter (in frames) to record experiment data. If save_interval is -1, nothing is recorded: int (default: 10)
        interaction_mode    -- whether the user can hover over a robot to have its gene data output on the console: bool (default: False)
        """

        self.save_filename = save_filename
        self.save_interval = save_interval

        self.max_iters = max_iters

        self.mng = HtgManager(
                pop_size=population_size,
                htg_method=htg_method,
                task=task,
                fitness_selection_method=fitness_selection_method,
                mutate_method= lambda x: flatMutate(x, 0.1),
                boundary_x=size[0],
                boundary_y=size[1],
                max_vel=robot_data['max_velocity'],
                sense_radius=robot_data['sense_radius'],
                num_neighbours=robot_data['max_neighbours'],
                diffuse_rate=robot_data['diffuse_rate'],
                act_rate=robot_data['act_rate'],
                nn_info=robot_data['nn_info']
                )

        self.mng.update()
        x,y,a,c = self.mng.getPopState()
        self.iters = 0

    def run(self):
        done = False

        with open(self.save_filename, "w") as fp:
            population = self.mng.pop
            genotypeLength = len(population[0].getGenotype())
            header = "iter,robot_idx,fitness"
            for i in range(genotypeLength):
                header += ",locus_{}".format(i)
            header += "\n"

            fp.write(header)


            while not done:

                # Data recorder
                if self.save_interval != -1:
                    if (self.iters + 1) % self.save_interval == 0:
                        ### save data
                        population = self.mng.pop
                        for i,p in enumerate(population):
                            line = "{},{},{}".format(self.iters, i, self.mng.fitnesses[i])
                            genes = population[i].getGenotype()
                            for g in genes:
                                line += ",{}".format(g)
                            line += "\n"
                            fp.write(line)

                if self.iters > self.max_iters:
                    break

                self.__tick__()

    def __tick__(self):

        ## sim update
        self.mng.update()

        self.iters += 1