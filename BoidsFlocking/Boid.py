import pymunk
import numpy as np
from pymunk import Vec2d


class Boid:
    def __init__(self, position: tuple[int, int], angle: float, scale: int = 1):
        self.shape_scale = scale
        self.body = None
        self.shape = None
        self.create(position, angle)

    def create(self, position: tuple[int, int], angle: float):
        triangle_vertices = [
            (0, 2 * self.shape_scale),
            (0, -2 * self.shape_scale),
            (6 * self.shape_scale, 0)
        ]
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = position
        self.body.angle = angle
        self.shape = pymunk.Poly(self.body, triangle_vertices)

    def accelerate(self, scale: int):
        x_velocity, y_velocity = np.cos(self.body.angle), np.sin(self.body.angle)
        self.body.velocity = Vec2d(x_velocity, y_velocity).normalized() * scale

    def stop(self):


class Flock:
    def __init__(self):
        pass
