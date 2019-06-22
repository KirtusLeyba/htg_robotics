import numpy as np

class robot:

	## TODO: So far i am only including 3*n spaces in the sensing vector,
	## so the robot can only sense other robots. We need to add the environmental
	## and state functionality as well! - Kirtus

	def __init__(self, x, y, r, n):
		self.x = x ## x floating point position
		self.y = y ## y floating point position
		self.r = r ## radius of sensing vector
		self.n = n ## number of neighbors to track in sensing vector
		self.w = 0.0 ## current angular velocity
		self.vx = 0.0 ## current x velocity
		self.vy = 0.0 ## current y velocity
		self.theta = 0.0 ## current angle

		self.s_size = 3*n ## size of sensing vector
		self.a_size = 3 ## size of action vector

		self.s = np.zeros(s_size) ## sensing vector
		self.a = np.zeros(a_size) ## action vector

		## Weights
		self.W = np.zeros((self.s_size, self.a_size))

	def calcAction(self):
		self.a = self.W*self.s

	def __hash__(self):
		return hash(str(self.x) + \
			"," + str(self.y) + \
			"," + str(self.s) + \
			"," + str(self.r))

	def __eq__(self, other):
		if(hash(self) == hash(other)):
			return True
		return False

