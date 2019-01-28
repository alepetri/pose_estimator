"""Module contains a quick and dirty simulator for position estimation.

Imports:
pygame
numpy
PoseEstimator from pose_estimator.py

Classes:
Rectangle -- stores information for custom pygame rectangle
Tricycle -- relates rectangles to form tricylce robot

Controls:
Up Arrow     -- move forward
Down Arrow   -- move backward
Left Arrow   -- move rotate steering wheel -yaw
Right Arrow  -- move rotate steering wheel +yaw

******************************************************************************
               WARNING! NOT PEP8 COMPLAINT! NOT FINE TUNED!
******************************************************************************
"""

import pygame
import numpy as np
from pose_estimator import PoseEstimator

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
            newX = (self.corners[i][0]-axis_point[0])*np.cos(-angle)-(self.corners[i][1]-axis_point[1])*np.sin(-angle)+axis_point[0]
            newY = (self.corners[i][1]-axis_point[1])*np.cos(-angle)+(self.corners[i][0]-axis_point[0])*np.sin(-angle)+axis_point[1]
            self.corners[i] = (newX, newY)
        self.calc_center()

    def translate(self, vector, speed):
        for i in range(4):
            self.corners[i] = (self.corners[i][0]+vector[0]*speed, self.corners[i][1]+vector[1]*speed)
        self.calc_center()

    def forward_vector(self):
        array = np.subtract(self.corners[1],self.corners[0])
        unit = tuple(array/np.sum(array**2)**0.5 + (0,))
        return unit

    def calc_center(self):
        self.center = ((self.corners[0][0]+self.corners[2][0])/2,(self.corners[0][1]+self.corners[2][1])/2)


class Tricycle(object):

    def __init__(self, surface, d=30, r=40, point_of_rotation=tuple([100,100]), direction=tuple([0,1,0]), speed=10):
        self.surface = surface
        self.point_of_rotation = point_of_rotation
        self.d = d
        self.r = r
        self.speed = speed
        self.direction = direction
        self.centers = self.calc_centers()
        left_wheel = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[0]), 8, 20)
        right_wheel = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[1]), 8, 20)
        front_wheel = Rectangle(surface, 1, tuple([255, 255, 0]), tuple(self.centers[2]), 8, 20)
        case = Rectangle(surface, 1, tuple([0, 255, 0]), tuple(self.centers[3]), self.d+30, self.r+40)
        self.rect = [left_wheel, right_wheel, front_wheel, case]
        self.front_wheel_angle = 0
        self.ticks = 0

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

    def rotate_all(self, diminished_speed):
        angle = np.arctan(np.divide(diminished_speed,self.r))
        self.point_of_rotation = tuple([sum(x)/2 for x in zip(self.rect[0].center,self.rect[1].center)])
        for i in range(4):
            self.rect[i].rotate(angle, self.point_of_rotation)

    def translate_all(self, vector, diminished_speed):
        for i in range(4):
            self.rect[i].translate(vector, diminished_speed)

    def drive(self, direction):
        front_wheel_vector = self.rect[2].forward_vector()
        vehicle_vector = self.rect[3].forward_vector()
        self.rotate_all(direction*self.speed*np.sin(self.front_wheel_angle))
        self.translate_all(vehicle_vector, direction*self.speed*np.cos(self.front_wheel_angle))
        self.ticks += 8.2*direction

    def turn_front_wheel(self, angle):
        self.front_wheel_angle += angle
        if -np.pi/2 <= self.front_wheel_angle <= np.pi/2:
            self.rect[2].rotate(angle, self.rect[2].center)
        else:
            self.front_wheel_angle -= angle


if __name__ == "__main__":

    FPS = 100

    BLACK = (0 , 0 , 0)
    GREEN = (0 , 255 , 0)

    pygame.init()
    screen = pygame.display.set_mode((500 , 500))
    pygame.transform.flip(screen, False, True)

    clock = pygame.time.Clock()

    tri = Tricycle(screen, 30, 40, tuple([0,0]), tuple([0,1,0]), 2)
    pose_est = PoseEstimator(1)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        for i in range(9):
            pygame.draw.line(screen, (0, 200, 200), (0, 50*(i+1)), (500, 50*(i+1)), 1)
            pygame.draw.line(screen, (0, 200, 200), (50*(i+1), 0), (50*(i+1), 500), 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            tri.drive(1)
        if keys[pygame.K_DOWN]:
            tri.drive(-1)
        if keys[pygame.K_LEFT]:
            tri.turn_front_wheel(np.pi/180)
        if keys[pygame.K_RIGHT]:
            tri.turn_front_wheel(-np.pi/180)
        tri.draw()
        print(pose_est.estimate(pygame.time.get_ticks(), tri.front_wheel_angle, tri.ticks, 0))

        pygame.display.flip()

    pygame.quit()
