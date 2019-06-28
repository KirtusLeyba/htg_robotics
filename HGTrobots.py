import numpy as np

class robot:

	## TODO: So far i am only including 5*n spaces in the sensing vector,
	## so the robot can only sense other robots. We need to add the environmental
	## and state functionality as well! - Kirtus

	def __init__(self, x, y, r, n, maxV):
		self.x = x ## x floating point position
		self.y = y ## y floating point position
		self.r = r ## radius of sensing vector
		self.n = n ## number of neighbors to track in sensing vector
		self.w = 0.0 ## current angular velocity
		self.vx = 0.0 ## current x velocity
		self.vy = 0.0 ## current y velocity
		self.theta = 0.0 ## current angle
		self.maxV = maxV
		self.neighbours = 0

		self.state_size = len(self.getState())
		self.s_size = (self.state_size+1)*n ## size of sensing vector 
																					#	(+1 for whether the robot is present)
		self.a_size = 2 ## size of action vector

		self.s = np.zeros(self.s_size) ## sensing vector
		self.a = np.zeros(self.a_size) ## action vector

		## Weights
		self.W = np.zeros((self.s_size, self.a_size))

	def distTo(self, other):
		return np.sqrt((self.x - other.x)**2 +\
		 (self.y - other.y)**2)

	def getState(self):
		return [
				self.x, self.y, self.vx, self.vy, self.theta
				]

	def getGenotype(self):
		gene = np.reshape(self.W, (-1))
		return gene

	def insertSubGene(self, subgene, idx):
		g = self.getGenotype()
		assert idx + len(subgene) < len(g), "subgene overflow"

		g[idx:(idx+len(subgene))] = subgene
		self.W = np.reshape(g, np.shape(self.W))

	def getNeighbours(self, robotList):
		ns = robotList[:]
		ns.sort(key = lambda x: self.distTo(x))
		ns_r = []
		for n in ns:
			if self.distTo(n) <= self.r:
				ns_r.append(n)
		neighs = ns_r[:self.n]
		self.neighbours = len(neighs)
		return neighs

	def calcSense(self, robotList):
		### find closest robots
		#robotList.sort(key = lambda x: self.distTo(x))
		ns = self.getNeighbours(robotList)
		sense_size = self.state_size + 1
		for i,r in enumerate(ns):
			idx = i*sense_size
			if self.distTo(r) <= self.r:
				self.s[idx:(idx+self.state_size)] = r.getState()
				self.s[idx+sense_size] = 1 # robot present
			else:
				self.s[idx:(idx+sense_size)] = [0]*sense_size # robot absent

	def calcAction(self):
		self.a = np.dot(self.s, self.W)
		try:
			self.a = self.z/np.sqrt(np.sum(self.a**2))
		except:
			self.a = self.a

	def takeAction(self):
		nextTheta = self.theta + self.a[0] 
		if(nextTheta > 2*np.pi):
			nextTheta = nextTheta - 2*np.pi
		elif nextTheta < 0.0:
				nextTheta += 2*np.pi
		self.theta = nextTheta

		currentV = np.sqrt(self.vx*self.vx + self.vy*self.vy)
		nextV = min(max(currentV + self.a[1], -self.maxV), self.maxV)

		self.vx = nextV*np.cos(self.theta)
		self.vy = nextV*np.sin(self.theta)

		self.x = self.x + self.vx
		self.y = self.y + self.vy

	def __hash__(self):
		return hash(str(self.x) + \
			"," + str(self.y) + \
			"," + str(self.s) + \
			"," + str(self.r))

	def __eq__(self, other):
		if(hash(self) == hash(other)):
			return True
		return False

