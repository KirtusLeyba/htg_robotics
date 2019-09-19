import numpy as np

class robot:

    ## TODO: So far i am only including 5*n spaces in the sensing vector,
    ## so the robot can only sense other robots. We need to add the environmental
    ## and state functionality as well! - Kirtus

    def __init__(self, x, y, r, n, maxV, boundary_x, boundary_y, ID, modular_weights=False):
        self.pos_x = x ## x floating point position
        self.pos_y = y ## y floating point position
        self.sense_radius = r ## radius of sensing vector
        self.num_neighbours = n ## number of neighbors to track in sensing vector
        self.angular_vel = 0.0 ## current angular velocity
        self.vel_x = 0.0 ## current x velocity
        self.vel_y = 0.0 ## current y velocity
        self.angle = 0.0 ## current angle
        self.max_vel = maxV
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y

        self.ang_vel = 0.0
        self.max_ang_vel = 0.3

        self.live_neighbours = 0

        self.state_size = len(self.getState())
        self.sensor_size_one_robot = self.state_size + 1
        self.sensor_size = self.sensor_size_one_robot*n ## size of sensing vector 
                                                                                                                                                                #	(+1 for whether the robot is present)
        self.action_size = 2 ## size of action vector

        self.sensors = np.zeros(self.sensor_size) ## sensing vector
        self.actions = np.zeros(self.action_size) ## action vector

        self.FRICTION = 0.9

        ## Weights
        self.modular_weights = modular_weights
        if self.modular_weights:
            # weights for each input channel are the same.
            self.weights = np.random.randn(self.sensor_size_one_robot, self.action_size)
        else:
            # weights for input channels are different (doesn't make sense in this context).
            self.weights = np.random.randn(self.sensor_size, self.action_size)
        self.num_weights = np.shape(self.weights)[0]*np.shape(self.weights)[1]
        self.bias = np.random.randn(self.action_size)
        #print(self.weights)

        self.ID = ID

    def equalTo(self, other):
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y

    def distTo(self, other):
        return np.sqrt((self.pos_x - other.pos_x)**2 +\
         (self.pos_y - other.pos_y)**2)

    def getState(self):
        return [
                self.pos_x / self.boundary_x, 
                self.pos_y / self.boundary_y, 
                # TODO: normalise the below
                self.vel_x / self.max_vel, self.vel_y / self.max_vel, self.angle
                ]

    def getGenotype(self):
        gene = np.hstack(
                (np.reshape(self.weights, (-1)),
                    self.bias))
        return gene

    def insertSubGene(self, subgene, idx):
        g = self.getGenotype()
        assert idx + len(subgene) < len(g), "subgene overflow"

        #print('---INSERTION!!! {} at {}'.format(subgene, idx))
        #print('before', g)

        # mutate the subgene slightly.
       # subgene = np.clip(subgene + np.random.randn() * 0.01, -2.0, 2.0)

        g[idx:(idx+len(subgene))] = subgene
        #print('after', g)
        w_section = g[:self.num_weights]
        b_section = g[self.num_weights:]
        self.weights = np.reshape(w_section, np.shape(self.weights))
        self.bias = np.reshape(b_section, np.shape(self.bias))

    def getNeighbours(self, robotList):
        ns = robotList[:]
        ns.sort(key = lambda x: self.distTo(x))
        ns_r = []
        for n in ns:
            if self.distTo(n) <= self.sense_radius and not self.equalTo(n):
                ns_r.append(n)
        neighs = ns_r[:self.num_neighbours]
        self.neighbours = len(neighs)
        return neighs

    def calcSense(self, robotList):
        ### find closest robots
        ns = self.getNeighbours(robotList)
        sense_size = self.state_size + 1
        #self.sensors[(sense_size-1)::sense_size] = 0
        self.sensors *= 0.0
        for i,r in enumerate(ns):
            idx = i*sense_size
            #if self.distTo(r) <= self.sense_radius:
            #TODO: make the sensing relative to the robot and not world coords.
            # make the pos relative to my pos.
            rstate = r.getState()
            #rstate[0] -= self.pos_x / self.boundary_x
            #rstate[1] -= self.pos_y / self.boundary_y
            self.sensors[idx:(idx+self.state_size)] = rstate
            self.sensors[idx+sense_size-1] = 1 # robot present
            #else:
            #    self.sensors[idx:(idx+sense_size)] = [0]*sense_size # robot absent
        #print(self.sensors)

    def calcAction(self):
        if self.modular_weights:
            w_mod = np.tile(self.weights, (self.num_neighbours, 1))
            self.actions = np.dot(self.sensors, w_mod) + self.bias
        else:
            self.actions = np.dot(self.sensors, self.weights) + self.bias

    def takeAction(self):
        #next_angle = self.angle + self.actions[0] 
        self.ang_vel *= self.FRICTION
        self.ang_vel = min(max(self.ang_vel + self.actions[0], -self.max_ang_vel), self.max_ang_vel)
        self.angle += self.ang_vel

        if self.angle > 2*np.pi:
            self.angle -= 2*np.pi
        elif self.angle < 0.0:
            self.angle += 2*np.pi
        #print(self.angle)

        #print(self.actions)
        current_vel = np.sqrt(self.vel_x*self.vel_x + self.vel_y*self.vel_y)
        current_vel *= self.FRICTION # small bit of friction to stop always accelerating.
        next_vel = min(max(current_vel + self.actions[1], -self.max_vel), self.max_vel)

        self.vel_x = next_vel*np.cos(self.angle)
        self.vel_y = next_vel*np.sin(self.angle)
        

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

    def __hash__(self):
        return hash(str(self.pos_x) + \
            "," + str(self.pos_y) + \
            "," + str(self.sensors) + \
            "," + str(self.sense_radius))

    def __eq__(self, other):
        if(hash(self) == hash(other)):
            return True
        return False

