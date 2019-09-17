import numpy as np

class Task:

    def __init__(self, min_fitness, max_fitness):
        self.min_fitness = min_fitness
        self.max_fitness = max_fitness

    def compute_fitness(self, population):
        pass

class TaskClump(Task):
    '''
    A simple task where all agents have to go to one point.
    '''

    def __init__(self, min_fitness, max_fitness):
        super().__init__(min_fitness, max_fitness)

    def compute_fitness(self, population):
        fitness_values = [self.min_fitness]*len(population)

        # TODO: until we make a population class instead of a robot class, this will be slow.
        for i,p in enumerate(population):
            dist_sum = 0.0
            ns = p.getNeighbours(population)
            for q in ns:
                dist = (abs(p.pos_x - q.pos_x) + abs(p.pos_y - q.pos_y)) / self.max_fitness
                dist_sum += dist

            if len(ns) > 0:
                fitness_values[i] = 1.0 - (dist_sum / p.num_neighbours)
            else:
                fitness_values[i] = self.min_fitness

        return fitness_values


