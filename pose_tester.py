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

    def __init__(self, surface, thickness=3, color=(0 , 255 , 0), center=tuple([0,0]), width=10, height=20):
        self.surface = surface
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
        self.corners = [(center[0]+(width/2),center[1]-(height/2)), (center[0]+(width/2),center[1]+(height/2)), (center[0]-(width/2),center[1]+(height/2)), (center[0]-(width/2),center[1]-(height/2))]

    def draw(self):
        pygame.draw.polygon(self.surface, self.color, self.corners, self.thickness)

    def rotate(self, angle, axis_point):
        for i in range(4):
            newX = (self.corners[i][0]-axis_point[0])*np.cos(angle)-(self.corners[i][1]-axis_point[1])*np.sin(angle)+axis_point[0]
            newY = (self.corners[i][1]-axis_point[1])*np.cos(angle)+(self.corners[i][0]-axis_point[0])*np.sin(angle)+axis_point[1]
            self.corners[i] = (newX, newY)
        print(self.corners)

    def translate(self, vector, speed):
        for i in range(4):
            self.corners[i] = (self.corners[i][0]+vector[0]*speed, self.corners[i][1]+vector[1]*speed)

    def forward_vector(self):
        array = np.subtract(self.corners[1],self.corners[0])
        unit = tuple(array/np.sum(array**2)**0.5 + (0,))
        print unit
        return unit


class Tricycle(object):

    def __init__(self, surface, d=30, r=40, point_of_rotation=tuple([100,100]), direction=tuple([0,1,0]), speed=10):
        self.surface = surface
        self.point_of_rotation = point_of_rotation
        self.d = d
        self.r = r
        self.speed = speed
        self.direction = direction
        self.centers = self.calc_centers()
        left_wheel = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[0]), 10, 20)
        right_wheel = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[1]), 10, 20)
        front_wheel = Rectangle(surface, 1, tuple([255, 255, 0]), tuple(self.centers[2]), 10, 20)
        case = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[3]), self.d+30, self.r+40)
        self.rect = [left_wheel, right_wheel, front_wheel, case]
        self.front_wheel_angle = 0

    def calc_centers(self):
        right_vector = tuple(np.cross(list(self.direction),[0,0,1])[0:2])
        left = tuple(np.subtract(self.point_of_rotation,tuple([self.d*x/2 for x in right_vector])))
        right = tuple(np.add(self.point_of_rotation,tuple([self.d*x/2 for x in right_vector])))
        front = tuple(np.add(self.point_of_rotation,tuple([self.r*x for x in self.direction[0:2]])))
        all = tuple(np.add(self.point_of_rotation,tuple([self.r*x/2 for x in self.direction[0:2]])))
        return [left, right, front, all]

    def draw(self):
        for i in range(4):
            self.rect[i].draw()

    def rotate_all(self, angle):
        for i in range(4):
            self.rect[i].rotate(angle, self.point_of_rotation)

    def translate_all(self, vector, diminished_speed):
        for i in range(4):
            self.rect[i].translate(vector, diminished_speed)

    def drive(self):
        front_wheel_vector = self.rect[2].forward_vector()
        vehicle_vector = self.rect[3].forward_vector()
        angle = np.arccos(np.divide(np.dot(front_wheel_vector[0:2],vehicle_vector[0:2]),4))
        self.rotate_all(angle)#change the angle to sin of something
        self.translate_all(vehicle_vector, self.speed*np.cos(angle))

    def turn_front_wheel(self, angle):
        self.front_wheel_angle += angle
        print(self.front_wheel_angle)
        if -np.pi/2 <= self.front_wheel_angle <= np.pi/2:
            self.rect[2].rotate(angle, self.centers[2])

if __name__ == "__main__":

    FPS = 1

    # define colors
    BLACK = (0 , 0 , 0)
    GREEN = (0 , 255 , 0)

    # initialize pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode((500 , 500))
    # for setting FPS
    clock = pygame.time.Clock()

    tri = Tricycle(screen, 30, 40, tuple([200,200]), tuple([0,1,0]), 2)

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

        tri.turn_front_wheel(np.pi/180)
        tri.drive()
        tri.draw()

        # flipping the display after drawing everything
        pygame.display.flip()

    pygame.quit()
