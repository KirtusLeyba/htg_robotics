from HTGmanager import HtgManager
from HTGmethods import selectGSCrandLength
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
import numpy as np

import pygame

pygame.init()

size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Petri Dish - A")

num_neighbours=5
mng = HtgManager(
        pop_size=100,
        htg_method=lambda x: selectGSCrandLength(x, min_length=2, max_length=4),
        boundary_x=size[0],
        boundary_y=size[1],
        max_vel=4.0,
        sense_radius=50.0,
        num_neighbours=num_neighbours,
        diffuse_rate=10,
        act_rate=1
        )

preset_colors = []
preset_colors.append([100.0, 100.0, 100.0])
rt = 255.0 / num_neighbours
if num_neighbours > 1:
    for i in range(num_neighbours):
        preset_colors.append([0.0, rt + rt*i, 0.0])
print(preset_colors)

mng.update()
x,y,a,c = mng.getPopState()
#print(x,y,a,c)

clock = pygame.time.Clock()
done = False
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((250, 220, 180))
    
    # step the simulation
    mng.update()
    # get the simulation state
    #xs,ys,angles,neighbs = mng.getPopState()
    # draw the simulation state
    rad_base = 5
    rad_view = mng.pop[0].sense_radius
    max_col = mng.pop[0].num_neighbours
    line_size =10 
    for i,r in enumerate(mng.pop):
        x = r.pos_x
        y = r.pos_y
        a = r.angle
        ns = r.neighbours
        # base col
        col = preset_colors[ns]
        #col = [neighbs[i]/max_col*255.0, 0.0, 0.0]
        #print(col)
        # body of robot
        try:
            pygame.draw.ellipse(screen, col, [x-rad_base, y-rad_base, rad_base*2, rad_base*2], 3)
        # sensory range of robot
            #pygame.draw.ellipse(screen, (240, 240, 240), [x-rad_view, y-rad_view, rad_view*2, rad_view*2], 3)
        except:
            print("BBBB!!", x, y, rad_view, rad_base)
            print(r.vel_x, r.vel_y, a, ns, r.weights, r.bias, r.sensors, r.actions)
        # draw direction of robot
        pygame.draw.line(screen, col, [x, y], [x + line_size*np.cos(a), y + line_size*np.sin(a)], 2)

    #pygame.draw.line(screen, (255, 0, 0), [0,0], [100, 100], 5)

    pygame.display.flip()

    clock.tick(10) # 60 FPS

pygame.quit()

