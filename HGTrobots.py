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

		self.s_size = 5*n ## size of sensing vector
		self.a_size = 2 ## size of action vector

		self.s = np.zeros(self.s_size) ## sensing vector
		self.a = np.zeros(self.a_size) ## action vector

		## Weights
		self.W = np.zeros((self.s_size, self.a_size))

	def distTo(self, other):
		return np.sqrt((self.x - other.x)*(self.x - other.x) +\
		 (self.y - other.y)*(self.y - other.y))

	def calcSense(self, robotList):
		### find closest robots
		robotList.sort(key = lambda x: self.distTo(x))
		for i in range(self.n):
			self.s[i] = robotList[i].x
			self.s[i+1] = robotList[i].y
			self.s[i+2] = robotList[i].vx
			self.s[i+3] = robotList[i].vy
			self.s[i+4] = robotList[i].theta

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
		self.theta = nextTheta

		currentV = np.sqrt(self.vx*self.vx + self.vy*self.vy)
		nextV = currentV + self.a[1]

		if(np.abs(nextV) > self.maxV):
			if(nextV) > 0:
				nextV = self.maxV
			else:
				nextV = -1.0*self.maxV

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

