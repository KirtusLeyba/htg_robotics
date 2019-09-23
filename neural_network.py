import numpy as np

class NeuralNetwork:

    def __init__(self, layers, activation=np.tanh):
        '''
        Just your simple, standard NN.
        '''

        self.weights = [
                np.random.randn(l1,l2) for l1,l2 in zip(layers[:-1], layers[1:])
                ]
        self.biases = [
                np.random.randn(b) for b in layers[1:]
                ]
        self.activations = [activation]*len(self.weights)

    def forward(self, x):

        for w,b,a in zip(self.weights, self.biases, self.activations):
            x = a(np.dot(x, w) + b)

        return x

    def getGenotype(self):
        gene = None
        for w,b in zip(self.weights, self.biases):
            if gene is None:
                gene = np.hstack((np.reshape(w, (-1)), b))
            else:
                gene = np.hstack((gene, np.reshape(w, (-1)), b))

        return gene

    def insertSubGene(self, subgene, idx):
        g = self.getGenotype()
        assert idx + len(subgene) < len(g), "subgene overflow"

        g[idx:(idx+len(subgene))] = subgene
        # put the gene back into the weights
        culm = 0
        for idx,(w,b) in enumerate(zip(self.weights, self.biases)):
            n_weights = np.shape(w)[0]*np.shape(w)[1]
            n_biases = np.shape(b)[0]
            w_section = g[culm:(culm+n_weights)]
            culm += n_weights
            b_section = g[culm:(culm+n_biases)]
            culm += n_biases
            self.weights[idx] = np.reshape(w_section, np.shape(w))
            self.biases[idx] = np.reshape(b_section, np.shape(b))

class NeuralNetworkModular(NeuralNetwork):

    def __init__(self, layers, num_modules, activation=np.tanh):
        '''
        A flippin' standard NN but with modular structure so that (input)
            channels share the same weights.
        '''
        super().__init__(layers, activation)
        self.num_modules = num_modules

        # recreate the bias, as it shouldn't be modular.
        self.biases = [
                np.random.randn(b*self.num_modules) for b in layers[1:-1]
                ]
        self.biases.append(np.random.randn(layers[-1]))

    def forward(self, x):
        #TODO: middle layers need to be double tiled
        for idx,(w,b,a) in enumerate(zip(self.weights, self.biases, self.activations)):
            if idx < len(self.weights) - 1:
                w_modular = np.tile(w, (self.num_modules, self.num_modules))
            else:
                w_modular = np.tile(w, (self.num_modules, 1))
            x = a(np.dot(x, w_modular) + b)

        return x

