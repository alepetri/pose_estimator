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
        self.corners = [(center_x+(width/2),center_y+(height/2)), (center_x+(width/2),center_y-(height/2)), (center_x-(width/2),center_y+(height/2)), (center_x-(width/2),center_y)-(height/2)]

    def draw(self):
        pygame.draw.polygon(surface, color, self.corners, thickness)

    def rotate(self, angle):
        self.corners[0] = self.corners[0]sdf

class Tricycle(object):

    def __init__(self)
