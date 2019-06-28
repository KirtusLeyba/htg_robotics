from HGTrobots import *
import numpy as np
import matplotlib.pyplot as plt

import time

numBots = 10
width = 100
height = 100
maxV = 1.0
n = 2
robots = []
for i in range(numBots):
    rx = np.random.randint(0,width)
    ry = np.random.randint(0,height)
    rW = np.random.random((5*n,2))-0.5
    r = robot(rx, ry, 4.0, n, maxV)
    r.W = rW
    robots.append(r)

iters = 20

plt.ion()
fig, ax = plt.subplots()
sc = ax.scatter([], [])
plt.xlim(-100, 100)
plt.ylim(-100, 100)
plt.draw()

for i in range(iters):
    x = []
    y = []
    for j in range(len(robots)):
        x.append(robots[j].x)
        y.append(robots[j].y)

        robots[j].takeAction()
        
    sc.set_offsets(np.c_[x,y])
    fig.canvas.draw_idle()
    plt.pause(0.01)

plt.show()
