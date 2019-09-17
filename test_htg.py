from HTGmanager import HtgManager
from HTGmethods import selectGSCrandLength
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import numpy as np

mng = HtgManager(
        pop_size=20,
        htg_method=lambda x: selectGSCrandLength(x, min_length=2, max_length=4)
        )

preset_colors = np.array([
        [1.0, 0.0, 0.0],
        [0.5, 0.1, 0.0],
        [0.5, 0.5, 0.0],
        [0.0, 0.5, 0.5],
        [0.0, 0.0, 1.0]
        ])

mng.update()
x,y,a,c = mng.getPopState()
print(x,y,a,c)

#### test simulation
xList = []
yList = []
angleList = []
neighbList = []
iters = 100
itersPerUpdate = 10
iterCount = itersPerUpdate
for i in range(iters):
    x = []
    y = []
    angles = []
    neighbs = []
    
    mng.update()
    x,y,angles,neighbs = mng.getPopState()
            
    if(iterCount <= 0):
        iterCount = itersPerUpdate
    
    iterCount -= 1
    
    xList.append(x)
    yList.append(y)
    angleList.append(angles)
    neighbList.append(neighbs)
    
arrowScale = 8.0
coScale = mng.pop[0].num_neighbours #30.0
backScale = 1.1
radiusSize = np.pi*(mng.pop[0].sense_radius*2)**2 # for some reason this isn't equivalent to pixel size.

def update_plot(i, dx, dy, ax, ar, angleList, neighbList):
    
    vertices = np.zeros((len(dx[0])*2, 2))
    
    for j in range(len(dx[i])):
        vertices[j,0] = dx[i][j]
        vertices[j,1] = dy[i][j]
        
        vertices[j + len(dx[i]),0] = dx[i][j]
        vertices[j + len(dx[i]),1] = dy[i][j]
    
    ax.set_offsets(vertices)
    sza = ax.get_sizes()
    sza[:len(sza)//2] = radiusSize
#     print(sza)
    ax.set_sizes(sza)
    
    #co = preset_colors(neighbList[i])
    co = np.transpose(np.tile(np.array(neighbList[i]), (3, 1)))/coScale#*5.0
    #print(co)
    #print(neighbList)
    #print(co)
    #cols = np.vstack((co, np.ones((np.shape(xList)[1], 3))/backScale))
    cols = np.vstack((np.ones((np.shape(xList)[1], 3))/backScale, 
                  co))
    ax.set_color(cols)
    return ax,

fig = plt.figure()
arrows = []
co = np.transpose(np.tile(np.array(neighbList[0]), (3, 1)))/coScale
cols = np.vstack((np.ones((np.shape(xList)[1], 3))/backScale, 
                  co))
ax = plt.scatter(xList[0]*2, yList[0]*2, s=np.ones(np.shape(xList)[1]*2)*coScale, 
                 c=cols)
print('DPI', fig.dpi)

ani = animation.FuncAnimation(fig, update_plot, frames=len(xList),
                              fargs=(xList, yList, ax, arrows, angleList, neighbList))
plt.show()
