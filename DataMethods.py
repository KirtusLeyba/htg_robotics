import numpy as np

class DataRecorder:

    def __init__(self, gene_size):

        self.gene_size = gene_size
        self.population_gene_history = None

    def add_population_tick(self, population):

        all_genes = np.zeros((len(population), self.gene_size, 1))
        for i,p in enumerate(population):
            all_genes[i, :, 0] = population[i].getGenotype()

        if self.population_gene_history is None:
            self.population_gene_history = all_genes
        else:
            self.population_gene_history = np.concatenate((self.population_gene_history, all_genes), axis=2)

    def save_population_history(self, filename):
        '''
        Saves a population of robots over time RxGxT (shape: (R, G, T)) into a .csv.
        '''

        if self.population_gene_history is not None:
            with open(filename, 'w') as f:
                f.write('# SHAPE: {}\n'.format(np.shape(self.population_gene_history)))

                for t in range(np.shape(self.population_gene_history)[2]):

                    np.savetxt(f, self.population_gene_history[:, :, t], fmt='%2.8f', delimiter=',')

                    f.write('# Time: {}\n'.format(t))

            print('POPULATION HISTORY SAVED! data size: {}'.format(np.shape(self.population_gene_history)))



