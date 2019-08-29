import pygame

class DataDisplay:

    def __init__(self, data_dict, position, color=[200.0, 0.0, 0.0], size=10):
        self.data_dict = data_dict

        self.position = position
        self.color = color
        self.size = size
        self.font = pygame.font.Font(None, self.size)

        self.text_strs = {}
        self.texts = {}

        self.create_text()

    def update_value(self, key, value):
        if self.data_dict[key] != value:
            self.data_dict[key] = value
            self.create_text()

    def create_text(self):

        #self.text_str = ''
        for k in self.data_dict.keys():
            #self.text_str += "{} : {} \n".format(k, self.data_dict[k]) 
            self.text_strs[k] = "{} : {}".format(k, self.data_dict[k])
            self.texts[k] = self.font.render(self.text_strs[k], True, self.color)

    def draw(self, screen):
        for i,k in enumerate(self.data_dict.keys()):
            pos_x = self.position[0]
            pos_y = self.position[1] + self.size*i # hacky..
            screen.blit(self.texts[k], (pos_x, pos_y))


