import sys
import pygame
import pymunk
import pymunk.pygame_util
from Flock import Flock
from UserInterface2 import UserInterface
import thorpy as tp
from time import time


def main():
    running = True
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 30
    dt = 1 / fps
    use_numba = True

    space = pymunk.Space()
    user_interface = UserInterface(window, WIDTH, HEIGHT, margin=50)
    simulation_parameters = user_interface.get_parameters()
    # print(simulation_parameters)

    check_boundaries = True
    horizontal_cyclic_boundary = False
    vertical_cyclic_boundary = True
    separation_active = True
    alignment_active = False
    cohesion_active = True
    horizontal_wall_active = True
    vertical_wall_active = True

    flock = Flock(
        simulation_parameters.boid_number, space,
        space_coordinates=(WIDTH, HEIGHT),
        boid_size=simulation_parameters.boid_size,
        speed_scale=simulation_parameters.speed_scale,
        speed_range=(simulation_parameters.speed_min, simulation_parameters.speed_max),
        speed_active=False,
        avoid_range=simulation_parameters.avoid_range,
        avoid_factor=simulation_parameters.avoid_factor,
        align_range=simulation_parameters.align_range,
        align_factor=simulation_parameters.align_factor,
        cohesion_range=simulation_parameters.cohesion_range,
        cohesion_factor=simulation_parameters.cohesion_factor,
        turn_margin=simulation_parameters.boundary_margin,
        turn_factor=simulation_parameters.boundary_factor
    )
    # number_of_bodies = 1300
    # flock = Flock(number_of_bodies, space,
    #               space_coordinates=(WIDTH, HEIGHT),
    #               boid_size=2,
    #               speed_scale=200,
    #               speed_range=(1, 2),
    #               speed_active=False,
    #               avoid_range=15,
    #               avoid_factor=2,
    #               align_range=100,
    #               align_factor=0.08,
    #               cohesion_range=50,# 200
    #               cohesion_factor=0.05, # 0.5
    #               turn_margin=80,
    #               turn_factor=20)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    fps_time = 0
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
                    simulation_parameters.speed_active = False
                    flock.stop_boids()
                else:
                    simulation_parameters.speed_active = True
                    flock.accelerate_boids()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                check_boundaries = not check_boundaries
                print(f'check_boundaries {check_boundaries}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                horizontal_cyclic_boundary = not horizontal_cyclic_boundary
                print(f'horizontal_cyclic_boundary {horizontal_cyclic_boundary}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                vertical_cyclic_boundary = not vertical_cyclic_boundary
                print(f'vertical_cyclic_boundary {vertical_cyclic_boundary}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                separation_active = not separation_active
                print(f'separation_active {separation_active}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                alignment_active = not alignment_active
                print(f'alignment_active {alignment_active}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                cohesion_active = not cohesion_active
                print(f'cohesion_active {cohesion_active}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                horizontal_wall_active = not horizontal_wall_active
                print(f'horizontal_wall_active {horizontal_wall_active}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                vertical_wall_active = not vertical_wall_active
                print(f'vertical_wall_active {vertical_wall_active}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                flock.reset_boids()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                use_numba = not use_numba
                print(f'use numba {use_numba}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                print(f'frame time: {fps_time:.6}')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(user_interface.get_parameters())
                print(simulation_parameters)
                print(flock.number_of_boids)
        if user_interface.get_parameters().values_changed:
            # print(simulation_parameters)
            # simulation_parameters = user_interface.get_parameters()
            # print(simulation_parameters)
            flock.update_parameters(simulation_parameters)
            simulation_parameters.values_changed = False
        if flock.speed_active:
            start = time()
            if use_numba:
                flock.update_boid_velocity_with_numba(
                    check_boundaries=check_boundaries,
                    horizontal_cyclic_boundary=horizontal_cyclic_boundary,
                    vertical_cyclic_boundary=vertical_cyclic_boundary,
                    separation_active=separation_active,
                    alignment_active=alignment_active,
                    cohesion_active=cohesion_active,
                    vertical_wall_active=vertical_wall_active,
                    horizontal_wall_active=horizontal_wall_active
                )
            else:
                flock.update_boid_velocity(
                    check_boundaries=check_boundaries,
                    horizontal_cyclic_boundary=horizontal_cyclic_boundary,
                    vertical_cyclic_boundary=vertical_cyclic_boundary,
                    separation_active=separation_active,
                    alignment_active=alignment_active,
                    cohesion_active=cohesion_active,
                    vertical_wall_active=vertical_wall_active,
                    horizontal_wall_active=horizontal_wall_active
                )
            fps_time = time() - start

        # user_interface.parameter_changed()
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