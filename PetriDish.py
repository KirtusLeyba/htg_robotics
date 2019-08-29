from HTGmanager import HtgManager
from HTGmethods import selectGSCrandLength, selectAll
from Task import TaskClump
from DataMethods import DataRecorder
import numpy as np

from dataDisplay import DataDisplay
from button import Button


import pygame

class PetriDish:

    def __init__(self,
            size = (400, 300),
            nametag = "A",
            population_size=50,
            robot_data = {
                'max_neighbours' :  5,
                'max_velocity' :    4.0,
                'sense_radius':     50.0,
                'diffuse_rate':     10, # TODO convert from timesteps to secs.
                'act_rate':         1, # TODO convert from timesteps to secs.
                },
            htg_method=lambda x: selectGSCrandLength(x, min_length=2, max_length=4),
            task=TaskClump(0, 100),
            fitness_selection_method=selectAll,
            visuals = {
                'colour_A'      : [100.0, 100.0, 100.0],
                'colour_B'      : [0.0, 225.0, 0.0],
                'background'    : [250.0, 220.0, 180.0],
                'draw_radius'   : False,
                'draw_transfer' : True
                },
            save_interval=-1,
            record_interval = 10,
            interaction_mode = False,
            ):
        """
        size                -- dimension of the screen: (float, float) (default: (400, 300))
        nametag             -- name of the experiment: string (default: "A")
        population_size     -- number of individuals: int (default: 50)
        robot_data          -- dict. of robot params: dictionary (default:
                    {
                        'max_neighbours' :  5,      -- max. number of neighbours a robot can see.
                        'max_velocity' :    4.0,    -- max. velocity a robot can reach.
                        'sense_radius':     50.0,   -- radius of sensory detection.
                        'diffuse_rate':     10,     -- ticks per gene diffusion.
                        'act_rate':         1,      -- ticks per robot action.
                    })
        htg_method          -- method describing how genes are selected.
        visuals             -- colours of graphics: dictionary (default:
                    {
                        'colour_A'          : [100.0, 100.0, 100.0],    -- colour when there are no neighbours.
                        'colour_B'          : [0.0, 225.0, 0.0],        -- colour when there are max. neighbours.
                        'background'        : [250.0, 220.0, 180.0]     -- colour of background.
                        'draw_radius'       : False                     -- whether to draw the visual radius of a robot.
                        'draw_transfer'     : True                      -- whether to draw the gene transfer lines.
                    })
        save_interval       -- how often (in frames) should the data of the population be saved. -1 means never: int (default: -1)
        record_interval     -- how ofter (in frames) to record experiment data. If save_interval is -1, nothing is recorded: int (default: 10)
        interaction_mode    -- whether the user can hover over a robot to have its gene data output on the console: bool (default: False)
        """

        pygame.init()

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Petri Dish - " + nametag)
        self.save_filename = 'outputs/' + 'population_data_' + nametag + '.txt'
        self.save_interval = save_interval
        self.record_interval = record_interval
        self.interaction_mode = interaction_mode

        self.mng = HtgManager(
                pop_size=population_size,
                htg_method=htg_method,
                task=task,
                fitness_selection_method=fitness_selection_method,
                boundary_x=size[0],
                boundary_y=size[1],
                max_vel=robot_data['max_velocity'],
                sense_radius=robot_data['sense_radius'],
                num_neighbours=robot_data['max_neighbours'],
                diffuse_rate=robot_data['diffuse_rate'],
                act_rate=robot_data['act_rate']
                )

        self.visuals = visuals
        self.preset_colors = []
        self.preset_colors.append(visuals['colour_A'])
        #rt = 225.0 / robot_data['max_neighbours'] + 100.0
        rt = [(b-a)/robot_data['max_neighbours'] for a,b in zip(visuals['colour_A'],visuals['colour_B'])]
        if robot_data['max_neighbours'] > 1:
            for i in range(1, robot_data['max_neighbours']+1):
                #self.preset_colors.append([0.0, rt + rt*i, 0.0])
                self.preset_colors.append([
                    visuals['colour_A'][0] + rt[0] * i, 
                    visuals['colour_A'][1] + rt[1] * i, 
                    visuals['colour_A'][2] + rt[2] * i])
        print(self.preset_colors)

        self.mng.update()
        x,y,a,c = self.mng.getPopState()

        self.fps = 60
        self.clock = pygame.time.Clock()

        ### robot statistics display
        self.robot_data = DataDisplay(
                {
                    'ID' : 10,
                    'POS': (10, 10),
                    #'GENE' : [1, 2, 3, 4, 5]
                    },
                position=[5.0, 5.0],
                color=[0.0, 0.0, 0.0],
                size=12,
                )
        self.pause_button = Button('||', [15.0, size[1] - 15.0], [100.0, 100.0, 100.0], 10)
        self.up_fps = Button('>', [30.0, size[1] - 15.0], [100.0, 100.0, 100.0], 10, toggle=False)
        self.down_fps = Button('<', [2.0, size[1] - 15.0], [100.0, 100.0, 100.0], 10, toggle=False)
        self.color_button = Button('=', [size[0] - 30.0, 7.0], [100.0, 100.0, 0.0], 15)
        self.color_data = DataDisplay(
                {
                    'VIS' : 'neighb.'
                    },
                position=[size[0] - 55.0, 0.0], 
                color=[100.0, 100.0, 0.0], 
                size=14
                )
        self.fps_data = DataDisplay(
                {
                    'FPS' : 60,
                    'PAUSE' : 'OFF'
                    },
                position=[45.0, size[1] - 22.0],
                color =[100.0, 100.0, 100.0],
                size=12
                )
        #self.pause_button = DataDisplay(
        #        {
        #            '|' : '|'
        #        },
        #        position=[0.0, size[1] - 20],
        #        color=[255.0, 255.0, 255.0],
        #        size = 20
        #        )

        # data recorder
        self.data_recorder = DataRecorder(gene_size=np.shape(self.mng.pop[0].getGenotype())[0])

        self.iters = 0

    def run(self):
        self.clock = pygame.time.Clock()
        done = False
        while not done:
           self.__tick__() 


        # a final save.
        self.data_recorder.add_population_tick(self.mng.pop)
        self.data_recorder.save_population_history(self.save_filename)

        pygame.quit()

    def __tick__(self):
        m_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                m_down = True

        mp_x, mp_y = pygame.mouse.get_pos()

        self.pause_button.mouse_over((mp_x, mp_y), m_down)
        self.up_fps.mouse_over((mp_x, mp_y), m_down)
        self.down_fps.mouse_over((mp_x, mp_y), m_down)
        self.color_button.mouse_over((mp_x, mp_y), m_down)

        self.screen.fill(self.visuals['background'])
        
        # step the simulation
        if not self.pause_button.on:
            self.mng.update()
            self.fps_data.update_value('PAUSE', 'OFF')
        else:
            self.fps_data.update_value('PAUSE', 'ON')

        # TODO: this is slow. Put all robot pos's in a matrix.
        #if self.iters % self.DATA_TICK_RATE == 0:
        if self.interaction_mode:
            for r in self.mng.pop:
                m_dist_sqrd = (mp_x - r.pos_x)**2 + (mp_y - r.pos_y)**2
                if m_dist_sqrd < 200.0:
                    self.robot_data.update_value('ID', r.ID)
                    self.robot_data.update_value('POS', (int(r.pos_x), int(r.pos_y)))
                    #self.robot_data.update_value('GENE', r.getGenotype())
                    print('ID: {}, GENE: {}'.format(r.ID, r.getGenotype()))
                    break

        if not self.color_button.on:
            self.color_data.update_value('VIS', 'neighb.')
        else:
            self.color_data.update_value('VIS', 'fitn.')

        self.fps_data.update_value('FPS', self.fps)

        self.__draw__()
        #pygame.draw.line(screen, (255, 0, 0), [0,0], [100, 100], 5)

        pygame.display.flip() # draw everything onto the screen.

    
        if self.up_fps.on:
            self.fps = min(60, self.fps + 5)
            print(self.fps)
        elif self.down_fps.on:
            self.fps = max(5, self.fps - 5)
            print(self.fps)

        # Data recorder
        if self.save_interval != -1:
            if (self.iters + 1) % self.record_interval == 0:
                self.data_recorder.add_population_tick(self.mng.pop)
            if (self.iters + 1) % self.save_interval == 0:
                self.data_recorder.save_population_history(self.save_filename)

        self.clock.tick(self.fps) # 60 FPS

        # freeze iteration counter.
        if not self.pause_button.on:
            self.iters += 1


    def __draw__(self):

        # get the simulation state
        rad_base = 5
        rad_view = self.mng.pop[0].sense_radius
        max_col = self.mng.pop[0].num_neighbours
        line_size =10 

        for i,r in enumerate(self.mng.pop):
            x = r.pos_x
            y = r.pos_y
            a = r.angle
            ns = r.neighbours
            # base col
            if self.color_button.on:
                if self.mng.fitnesses is not None:
                    col = (0.0, 0.0, self.mng.fitnesses[i]*255.0)
                else:
                    col = [0.0, 0.0, 0.0]
            else:
                col = self.preset_colors[ns]
            #col = [neighbs[i]/max_col*255.0, 0.0, 0.0]
            #print(col)
            # body of robot
            try:
                pygame.draw.ellipse(self.screen, col, [x-rad_base, y-rad_base, rad_base*2, rad_base*2], 3)
            # sensory range of robot
                if self.visuals['draw_radius']:
                    pygame.draw.ellipse(screen, (240, 240, 240), [x-rad_view, y-rad_view, rad_view*2, rad_view*2], 3)
            except:
                print("BBBB!!", x, y, rad_view, rad_base)
                print(r.vel_x, r.vel_y, a, ns, r.weights, r.bias, r.sensors, r.actions)
            # draw direction of robot
            pygame.draw.line(self.screen, col, [x, y], [x + line_size*np.cos(a), y + line_size*np.sin(a)], 1)

        # draw the diffusion lines.
        if self.visuals['draw_transfer']:
            diff_tick = self.mng.diffuse_history[-1]
            for d in diff_tick:
                idA = d[0]
                #print(d)
                posA = (self.mng.pop[idA].pos_x, self.mng.pop[idA].pos_y)
                idB = d[1]
                posB = (self.mng.pop[idB].pos_x, self.mng.pop[idB].pos_y)
                sub_gene = d[2]
                sub_gene_idx = d[3]

                pygame.draw.line(self.screen, [200.0, 0.0, 0.0], posA, posB, 2)

        # draw data
        self.robot_data.draw(self.screen)
        self.fps_data.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.up_fps.draw(self.screen)
        self.down_fps.draw(self.screen)
        self.color_button.draw(self.screen)
        self.color_data.draw(self.screen)

