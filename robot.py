import numpy as np

class robot:

	## TODO: So far i am only including 3*n spaces in the sensing vector,
	## so the robot can only sense other robots. We need to add the environmental
	## and state functionality as well! - Kirtus

	def __init__(self, x, y, r, n):
		self.pos_x = x ## x floating point position
		self.pos_y = y ## y floating point position
		self.sense_radius = r ## radius of sensing vector
		self.num_neighbours = n ## number of neighbors to track in sensing vector
		self.angular_vel = 0.0 ## current angular velocity
		self.vel_x = 0.0 ## current x velocity
		self.vel_y = 0.0 ## current y velocity
		self.angle = 0.0 ## current angle

		self.sensor_size = 3*n ## size of sensing vector
		self.action_size = 3 ## size of action vector

		self.sensors = np.zeros(s_size) ## sensing vector
		self.actions = np.zeros(a_size) ## action vector

		## Weights
		self.weights = np.zeros((self.s_size, self.a_size))

	def calcAction(self):
		self.actions = np.dot(self.sensors, self.weights)

	def __hash__(self):
		return hash(str(self.pos_x) + \
			"," + str(self.pos_y) + \
			"," + str(self.sensors) + \
			"," + str(self.sense_radius))

	def __eq__(self, other):
		if(hash(self) == hash(other)):
			return True
		return False

