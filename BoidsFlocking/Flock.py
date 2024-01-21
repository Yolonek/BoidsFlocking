import pymunk
import pygame
import numpy as np
import numba as nb
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

    def change_velocity(self, vx: float, vy: float, vmax: int, vmin: int):
        self.body.angle = np.arctan2(-vx, vy) + np.pi / 2
        velocity = Vec2d(vx, vy)
        speed = abs(velocity)
        if speed >= vmax:
            self.body.velocity = velocity.normalized() * vmax
            self.speed = vmax
        elif speed < vmin:
            self.body.velocity = velocity.normalized() * vmin
            self.speed = vmin
        else:
            self.body.velocity = velocity
            self.speed = speed

    def accelerate(self):
        x_velocity, y_velocity = np.cos(self.body.angle), np.sin(self.body.angle)
        self.body.velocity = Vec2d(x_velocity, y_velocity) * self.speed

    def stop(self):
        self.speed = abs(self.body.velocity)
        self.body.velocity = Vec2d(0, 0)

    def check_boundaries(self, WIDTH: int, HEIGHT: int,
                         cyclic_horizontal: bool = True, cyclic_vertical: bool = True):
        if cyclic_horizontal:
            if self.body.position[0] >= WIDTH:
                self.body.position = (0, self.body.position[1])
            elif self.body.position[0] <= 0:
                self.body.position = (WIDTH, self.body.position[1])
        else:
            if self.body.position[0] > WIDTH:
                self.body.position = (WIDTH, self.body.position[1])
            elif self.body.position[0] < 0:
                self.body.position = (0, self.body.position[1])

        if cyclic_vertical:
            if self.body.position[1] >= HEIGHT:
                self.body.position = (self.body.position[0], 0)
            elif self.body.position[1] <= 0:
                self.body.position = (self.body.position[0], HEIGHT)
        else:
            if self.body.position[1] > HEIGHT:
                self.body.position = (self.body.position[0], HEIGHT)
            elif self.body.position[1] < 0:
                self.body.position = (self.body.position[0], 0)


class Flock:
    def __init__(self, number_of_boids: int, scale: int,
                 space: pymunk.Space,
                 space_coordinates: tuple[int, int],
                 coordinates: tuple[int, int] = None,
                 speed_range: tuple[int, int] = (1, 3),
                 speed_scale: int = 100,
                 avoid_range: int = 10,
                 avoid_factor: float = 0.05,
                 align_range: int = 50,
                 align_factor: float = 0.05,
                 cohesion_range: int = 50,
                 cohesion_factor: float = 0.05,
                 turn_margin: int = 50,
                 turn_factor: int = 1):
        self.number_of_boids = number_of_boids
        self.boids = []
        self.boid_scale = scale
        self.WIDTH = space_coordinates[0]
        self.HEIGHT = space_coordinates[1]
        self.space = space
        self.speed_active = False
        self.speed_min, self.speed_max = Vec2d(*speed_range) * speed_scale
        self.speed_scale = speed_scale
        self.avoid_range = avoid_range
        self.avoid_factor = avoid_factor
        self.align_range = align_range
        self.align_factor = align_factor
        self.cohesion_range = cohesion_range
        self.cohesion_factor = cohesion_factor
        self.turn_margin = turn_margin
        self.turn_factor = turn_factor
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
                        speed=self.speed_scale)
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

    def update_boid_velocity(self,
                             check_boundaries: bool,
                             horizontal_cyclic_boundary: bool,
                             vertical_cyclic_boundary: bool,
                             separation_active: bool,
                             alignment_active: bool,
                             cohesion_active: bool,
                             vertical_wall_active: bool,
                             horizontal_wall_active: bool):
        for boid in self.boids:
            if check_boundaries:
                boid.check_boundaries(self.WIDTH, self.HEIGHT,
                                      cyclic_horizontal=horizontal_cyclic_boundary,
                                      cyclic_vertical=vertical_cyclic_boundary)
            if any([separation_active, alignment_active, cohesion_active, vertical_wall_active, horizontal_wall_active]):
                close_dx, close_dy = 0, 0
                xvel_avg, yvel_avg, neighboring_boids_align = 0, 0, 0
                xpos_avg, ypos_avg, neighboring_boids_cohesion = 0, 0, 0
                boid_x, boid_y = boid.body.position
                for other in self.boids:
                    if other != boid:
                        other_x, other_y = other.body.position
                        boid_distance = distance.euclidean(boid.body.position, other.body.position)
                        if separation_active and boid_distance < self.avoid_range:
                            # boid_x, boid_y = boid.body.position
                            close_dx += boid_x - other_x
                            close_dy += boid_y - other_y

                        if alignment_active and boid_distance < self.align_range:
                            xvel_avg += other.body.velocity[0]
                            yvel_avg += other.body.velocity[1]
                            neighboring_boids_align += 1

                        if cohesion_active and boid_distance < self.cohesion_range:
                            xpos_avg += other_x
                            ypos_avg += other_y
                            neighboring_boids_cohesion += 1

                separation_vx, separation_vy = 0, 0
                if separation_active:
                    separation_vx = close_dx * self.avoid_factor
                    separation_vy = close_dy * self.avoid_factor

                alignment_vx, alignment_vy = 0, 0
                if neighboring_boids_align > 0 and alignment_active:
                    alignment_vx = ((xvel_avg / neighboring_boids_align) - boid.body.velocity[0]) * self.align_factor
                    alignment_vy = ((yvel_avg / neighboring_boids_align) - boid.body.velocity[1]) * self.align_factor

                cohesion_vx, cohesion_vy = 0, 0
                if neighboring_boids_cohesion > 0 and cohesion_active:
                    cohesion_vx = ((xpos_avg / neighboring_boids_cohesion) - boid_x) * self.cohesion_factor
                    cohesion_vy = ((ypos_avg / neighboring_boids_cohesion) - boid_y) * self.cohesion_factor

                wall_vx = 0
                if horizontal_wall_active:
                    if boid_x < self.turn_margin:
                        wall_vx = self.turn_factor
                    elif boid_x > self.WIDTH - self.turn_margin:
                        wall_vx = -self.turn_factor

                wall_vy = 0
                if vertical_wall_active:
                    if boid_y < self.turn_margin:
                        wall_vy = self.turn_factor
                    elif boid_y > self.HEIGHT - self.turn_margin:
                        wall_vy = -self.turn_factor

                boid.change_velocity(
                    boid.body.velocity[0] + separation_vx + alignment_vx + cohesion_vx + wall_vx,
                    boid.body.velocity[1] + separation_vy + alignment_vy + cohesion_vy + wall_vy,
                    self.speed_max, self.speed_min
                )

#
# def update_velocity_flock(flock, width, height, check_boundaries, separation_active, alignment_active, cohesion_active,
#                           avoid_range, avoid_factor, align_range, align_factor, cohesion_range, cohesion_factor):
#     for boid in flock:
#         if any([separation_active, alignment_active, cohesion_active]):
#             close_dx, xlose_dy = 0, 0
#             xvel_avg, yvel_avg, neighboring_boids_align = 0, 0, 0
#             xpos_avg, ypos_avg, neighboring_boids_cohesion = 0, 0, 0
#             for other in flock:
#                 if other != boid:
#                     boid_distance = np.sqrt(((boid[0] - other[0]) ** 2) + ((boid[1] - other[1]) ** 2))

if __name__ == '__main__':
    a, b, c = 10, 11, 10
    print(id(a), id(b), id(c))
    d = [a, b, c]
    print(id(d[0]), id(d[1]), id(d[2]))
    for i in d:
        print(id(i))
        print(id(i) is id(d[2]))





