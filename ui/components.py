import pygame
from globals import black, SCREEN_WIDTH
from math import cos, sin, pi, sqrt, asin
import time


class Pendulum:
    def __init__(self):
        self.length = 150
        self.radius = 20
        self.x = SCREEN_WIDTH // 4
        self.y = self.length + self.radius
        self.color = black
        self.amplitude = 100
        self.g = 400
        self.angle = 0
        self.pivot_point = (SCREEN_WIDTH // 4, 50)
        self.start_time = time.time()

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.pivot_point, 10)
        pygame.draw.line(win, self.color, self.pivot_point, (self.x, self.y), 5)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def change_pos(self):
        self.x = self.pivot_point[0] + (self.length * sin(self.angle))
        self.y = self.pivot_point[1] + (self.length * cos(self.angle))

    def move(self):
        period = 2 * pi * sqrt(self.length / self.g)
        angular_frequency = 2 * pi / period
        t = time.time() - self.start_time
        # mx_an = asin(self.amplitude/self.length)
        # self.angle = mx_an * cos(angular_frequency*t)
        y = self.amplitude * sin(angular_frequency * t)
        self.angle = asin(y / self.length)
        self.change_pos()

    def graph(self):
        period = 2 * pi * sqrt(self.length / self.g)
        angular_frequency = 2 * pi / period
        t = time.time() - self.start_time
        y = self.amplitude * sin(angular_frequency * t)
        a = -(angular_frequency**2) * self.amplitude * sin(angular_frequency * t)
        v = angular_frequency * self.amplitude * cos(angular_frequency * t)
        return [t, y, a, v]

    def set_values(self, vals):
        self.__init__()
        self.amplitude, self.length, self.g = vals


