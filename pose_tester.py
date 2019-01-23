'''
Written by Andy Lepetri

Controls:

Up Arrow     is move forward
Down Arrow   is move backward
Left Arrow   is move rotate steering wheel -yaw
Right Arrow  is move rotate steering wheel +yaw
'''

import pygame
import numpy as np
import math

class Rectangle(object):

    def __init__(self, surface, thickness=3, color=(0 , 255 , 0), center_x=0, center_y=0, width=10, height=20):
        self.center = (center_x, center_y)
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.thickness = thickness
        self.corners = [(center_x+(width/2),center_y-(height/2)), (center_x+(width/2),center_y+(height/2)), (center_x-(width/2),center_y+(height/2)), (center_x-(width/2),center_y-(height/2))]

    def draw(self):
        pygame.draw.polygon(self.surface, self.color, self.corners, self.thickness)

    def rotate(self, angle, axis_point):
        for i in range(4):
            newX = (self.corners[i][0]-axis_point[0])*np.cos(angle)-(self.corners[i][1]-axis_point[1])*np.sin(angle)+axis_point[0]
            newY = (self.corners[i][1]-axis_point[1])*np.cos(angle)+(self.corners[i][0]-axis_point[0])*np.sin(angle)+axis_point[1]
            self.corners[i] = (newX, newY)

    def translate(self, vector):
        for i in range(4):
            self.corners[i] = (self.corners[i][0]+vector[0], self.corners[i][1]+vector[1])

    def top_facing_unit_vector(self):
        dir_vector = tuple(np.subtract(self.corners[1],self.corners[0]))



class Tricycle(object):

    def __init__(self):


if __name__ == "__main__":

    FPS = 30

    # define colors
    BLACK = (0 , 0 , 0)
    GREEN = (0 , 255 , 0)

    # initialize pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode((500 , 500))
    # for setting FPS
    clock = pygame.time.Clock()

    rect = Rectangle(screen, 3, GREEN, 250, 250, 20, 60)

    # define a surface (RECTANGLE)
    # keep rotating the rectangle until running is set to False
    running = True
    while running:
        # set FPS
        clock.tick(FPS)
        # clear the screen every time before drawing new objects
        screen.fill(BLACK)
        # check for the exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        rect.rotate(np.pi/180, (250,250))
        rect.translate((1,-1))
        rect.draw()

        # flipping the display after drawing everything
        pygame.display.flip()

    pygame.quit()
