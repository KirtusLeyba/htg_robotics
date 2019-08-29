import numpy as np

from HGTrobots import robot

class HtgManager:

    def __init__(self, 
            pop_size, htg_method, task,
            fitness_selection_method,
            boundary_x=100, boundary_y=100, 
            max_vel=4.0, sense_radius=50.0,
            num_neighbours=5, diffuse_rate=10,
            act_rate=1):
        """
        boundary_x : int
            - furthest x-position.
        boundary_y : int
            - furthest y-position.
        max_vel : float
            - maximum velocity of the robot(s).
        sense_radius : float
            - maximum sensing range of the robot(s).
        num_neighbours : int
            - maximum number of neighbours a robot can sense.
        diffuse_rate : int
            - rate at which genes are diffused to neighbours.
        act_rate : int
            - rate at which robots act.
        """

        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.max_vel = max_vel
        self.sense_radius = sense_radius
        self.num_neighbours = num_neighbours

        self.pop_size = pop_size
        self.pop = []
        self.randomisePopulation()

        self.htg_method = htg_method
        self.task = task
        self.fitness_selection_method = fitness_selection_method

        self.act_rate = act_rate
        self.diffuse_rate = diffuse_rate

        self.diffuse_history = [] 

        self.iters = 0


    def randomisePopulation(self):
        self.pop = []
        for p in range(self.pop_size):
            r = robot(
                    x = np.random.randint(self.boundary_x),
                    y = np.random.randint(self.boundary_y),
                    #r = 20.0, #np.random.rand()*np.pi*2.0,
                    r = self.sense_radius, #np.random.rand()*np.pi*2.0,
                    n = self.num_neighbours, #self.pop_size,
                    maxV = self.max_vel,
                    boundary_x = self.boundary_x,
                    boundary_y = self.boundary_y,
                    ID = p
                    )
            r.weights = np.random.randn(*np.shape(r.weights))
            self.pop.append(r)

    def update(self):

        # start a new history recording.
        if self.iters % self.diffuse_rate == 0:
            self.diffuse_history.append([])

        # general robot update.
        for i in range(self.pop_size):
            # move robot.
            if self.iters % self.act_rate == 0:
                self.pop[i].calcSense(self.pop[:])
                self.pop[i].calcAction()
                self.pop[i].takeAction()
            # diffuse robot.
            #if self.iters % self.diffuse_rate == 0:
            #    self.diffuse(i)

            # check if the robot is outside of the boundary:
            if self.pop[i].pos_x > self.boundary_x:
                self.pop[i].pos_x = self.boundary_x
                self.pop[i].vel_x = abs(self.pop[i].vel_x) * -1.0
            elif self.pop[i].pos_x < 0:
                self.pop[i].pos_x = 0
                self.pop[i].vel_x = abs(self.pop[i].vel_x)

            if self.pop[i].pos_y > self.boundary_y:
                self.pop[i].pos_y = self.boundary_y
                self.pop[i].vel_y = abs(self.pop[i].vel_y) * -1.0
            elif self.pop[i].pos_y < 0:
                self.pop[i].pos_y = 0
                self.pop[i].vel_y = abs(self.pop[i].vel_y)

        # compute fitness.
        fitnesses = self.task.compute_fitness(self.pop)
        #print(fitnesses)
        min_fitness = np.min(fitnesses)
        max_fitness = np.max(fitnesses)
        avg_fitness = np.mean(fitnesses)
        print('min: {}, max: {}, avg: {}'.format(min_fitness, max_fitness, avg_fitness))
        # select robots to diffuse.
        diffuse_idxs = self.fitness_selection_method(fitnesses)
        # diffuse.
        if self.iters % self.diffuse_rate == 0:
            for i in diffuse_idxs:
                self.diffuse(i)

        self.iters += 1

    def diffuse(self, p_idx):
        ns = self.pop[p_idx].getNeighbours(self.pop)
        if len(ns) > 0:
            rand_idx = np.random.randint(len(ns))
            rand_n = ns[rand_idx]
            sub_gene, sub_gene_idx = self.htg_method(self.pop[p_idx].getGenotype())
            rand_n.insertSubGene(sub_gene, sub_gene_idx)

            self.diffuse_history[-1].append(
                    (self.pop[p_idx].ID, rand_n.ID, sub_gene, sub_gene_idx)
                        )

    def getPopState(self):
        xs = []
        ys = []
        ags = []
        neighbs = []
        for r in self.pop:
            xs.append(r.pos_x)
            ys.append(r.pos_y)
            ags.append(r.angle)
            neighbs.append(r.neighbours)

        #print(neighbs)

        return xs, ys, ags, neighbs


