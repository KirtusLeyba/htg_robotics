import numpy as np

from HGTrobots import robot

class HtgManager:

    def __init__(self, pop_size, htg_method, boundary_x=100, boundary_y=100):

        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.maxV = 4.0 #TODO

        self.pop_size = pop_size
        self.pop = []
        self.randomisePopulation()

        self.htg_method = htg_method

        self.act_rate = 1
        self.diffuse_rate = 10

        self.iters = 1


    def randomisePopulation(self):
        self.pop = []
        for p in range(self.pop_size):
            r = robot(
                    x = np.random.randint(self.boundary_x),
                    y = np.random.randint(self.boundary_y),
                    r = 50.0, #np.random.rand()*np.pi*2.0,
                    n = self.pop_size,
                    maxV = self.maxV,
                    )
            r.W = np.random.randn(*np.shape(r.W))
            self.pop.append(r)

    def update(self):
        for i in range(self.pop_size):
            if self.iters % self.act_rate == 0:
                self.pop[i].calcSense(self.pop[:])
                self.pop[i].calcAction()
                self.pop[i].takeAction()
            if self.iters % self.diffuse_rate == 0:
                self.diffuse(i)

        self.iters += 1

    def diffuse(self, p_idx):
        ns = self.pop[p_idx].getNeighbours(self.pop)
        if len(ns) > 0:
            rand_n = ns[np.random.randint(len(ns))]
            sub_gene, sub_gene_idx = self.htg_method(self.pop[p_idx].getGenotype())
            self.pop[p_idx].insertSubGene(sub_gene, sub_gene_idx)

    def getPopState(self):
        xs = []
        ys = []
        ags = []
        neighbs = []
        for r in self.pop:
            xs.append(r.x)
            ys.append(r.y)
            ags.append(r.theta)
            neighbs.append(r.neighbours)

        return xs, ys, ags, neighbs


