import pymunk
import pygame
import numpy as np
from pymunk import Vec2d
from scipy.spatial import distance


class Boid:
    def __init__(self, position: tuple[int, int], angle: float,
                 scale: int = 1, speed: int = 1):
        self.body = None
        self.shape = None
        self.saved_speed = Vec2d(0, 0)
        self.speed = speed
        self.create(position, angle, scale)

    def create(self, position: tuple[int, int], angle: float, scale: int):
        triangle_vertices = [
            (0, 2 * scale),
            (0, -2 * scale),
            (6 * scale, 0)
        ]
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = position
        self.body.angle = angle
        self.shape = pymunk.Poly(self.body, triangle_vertices)

    def change_speed(self, speed: int):
        self.speed = speed

    def change_velocity(self, vx: float, vy: float):
        self.body.angle = np.arctan2(-vx, vy) + np.pi / 2
        self.body.velocity = Vec2d(vx, vy).normalized() * self.speed

    def accelerate(self):
        x_velocity, y_velocity = np.cos(self.body.angle), np.sin(self.body.angle)
        self.body.velocity = Vec2d(x_velocity, y_velocity).normalized() * self.speed

    def stop(self):
        self.body.velocity = Vec2d(0, 0)

    def check_boundaries(self, WIDTH: int, HEIGHT: int):
        if self.body.position[0] >= WIDTH:
            self.body.position = (0, self.body.position[1])
        elif self.body.position[0] <= 0:
            self.body.position = (WIDTH, self.body.position[1])
        if self.body.position[1] >= HEIGHT:
            self.body.position = (self.body.position[0], 0)
        elif self.body.position[1] <= 0:
            self.body.position = (self.body.position[0], HEIGHT)


class Flock:
    def __init__(self, number_of_boids: int, scale: int,
                 space: pymunk.Space,
                 space_coordinates: tuple[int, int],
                 coordinates: tuple[int, int] = None,
                 average_speed: int = 1,
                 protected_range: int = 10,
                 avoid_factor: float = 0.05):
        self.number_of_boids = number_of_boids
        self.boids = []
        self.boid_scale = scale
        self.WIDTH = space_coordinates[0]
        self.HEIGHT = space_coordinates[1]
        self.space = space
        self.speed_active = False
        self.average_speed = average_speed
        self.protected_range = protected_range
        self.avoid_factor = avoid_factor
        if coordinates is not None:
            self.place_boids_from_list(coordinates)
        else:
            self.create_boids()

    def create_boids(self):
        for _ in range(self.number_of_boids):
            boid = Boid((np.random.randint(self.WIDTH),
                         np.random.randint(self.HEIGHT)),
                        np.random.random() * 2 * np.pi,
                        scale=self.boid_scale,
                        speed=self.average_speed)
            self.space.add(boid.body, boid.shape)
            self.boids.append(boid)

    def place_boids_from_list(self, coordinates: tuple[int, int]):
        pass

    def accelerate_boids(self):
        for boid in self.boids:
            boid.accelerate()
        self.speed_active = True

    def stop_boids(self):
        for boid in self.boids:
            boid.stop()
        self.speed_active = False

    def update_boid_parameter(self,
                              check_boundaries: bool,
                              separation_active: bool,
                              alignment_active: bool):
        for boid in self.boids:
            if check_boundaries:
                boid.check_boundaries(self.WIDTH, self.HEIGHT)
            if separation_active:
                close_dx = 0
                close_dy = 0
                for other in self.boids:
                    if other != boid:
                        boid_x, boid_y = boid.body.position
                        if distance.euclidean(boid.body.position, other.body.position) < self.protected_range:
                            close_dx += boid_x - other.body.position[0]
                            close_dy += boid_y - other.body.position[1]
                boid.change_velocity(
                    boid.body.velocity[0] + (close_dx * self.avoid_factor),
                    boid.body.velocity[1] + (close_dy * self.avoid_factor)
                )
            if alignment_active:
                pass


if __name__ == '__main__':
    print(any([False, True]))





