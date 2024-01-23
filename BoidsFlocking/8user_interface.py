import sys
import pygame
import pymunk
import pymunk.pygame_util
from Flock import Flock
from UserInterface import UserInterface
import thorpy as tp


def main():
    running = True
    pygame.init()
    WIDTH, HEIGHT = 1900, 1000
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 30
    dt = 1 / fps

    velocity_scale = 200
    body_scale = 5

    user_interface = UserInterface(window, WIDTH, HEIGHT, margin=50)

    space = pymunk.Space()

    number_of_bodies = 60
    flock = Flock(number_of_bodies, body_scale, space,
                  space_coordinates=(WIDTH, HEIGHT),
                  speed_scale=velocity_scale,
                  speed_range=(1, 3),
                  avoid_range=30,
                  avoid_factor=0.5,
                  align_range=100,
                  align_factor=0.005,
                  cohesion_range=200,
                  cohesion_factor=0.5,
                  turn_margin=200,
                  turn_factor=20)


    draw_options = pymunk.pygame_util.DrawOptions(window)

    while running:
        mouse_rel = pygame.mouse.get_rel()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if user_interface.get_menu_state():
                    user_interface.deactivate_menu()
                else:
                    user_interface.activate_menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if flock.speed_active:
                    flock.stop_boids()
                else:
                    flock.accelerate_boids()
        if flock.speed_active:
            flock.update_boid_velocity(
                check_boundaries=True,
                horizontal_cyclic_boundary=True,
                vertical_cyclic_boundary=True,
                separation_active=False,
                alignment_active=False,
                cohesion_active=False,
                vertical_wall_active=False,
                horizontal_wall_active=False
            )

        window.fill((11, 11, 11))
        space.debug_draw(draw_options)
        user_interface.update(events, mouse_rel)
        pygame.display.update()
        space.step(dt)
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    # sys.exit(main())
    main()