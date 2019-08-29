import pygame

class Button:

    def __init__(self, text, position, color, size, toggle=True):

        self.font = pygame.font.Font(None, size*2)
        self.text = self.font.render(text, True, color)
        self.position = position
        self.size = size
        self.on = False
        self.detect_on = True
        self.toggle = toggle

    def mouse_over(self, mouse_pos, mouse_down):

        dist_sqrd = (self.position[0] - mouse_pos[0])**2 + (self.position[1] - mouse_pos[1])**2

        # turn the button off at the start if not toggle mode.
        if not self.toggle:
            self.on = False

        if not mouse_down:
            self.detect_on = True

        if dist_sqrd < self.size**2:
            if mouse_down and self.detect_on:
                self.on = not self.on
                self.detect_on = False

    def draw(self, screen):
        screen.blit(self.text, self.position)
