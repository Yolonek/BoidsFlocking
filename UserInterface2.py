import pygame
import thorpy as tp
from dataclasses import dataclass
from functools import partial


@dataclass
class BoidFlockingParameters:
    boid_number: int = 100
    boid_size: int = 5

    speed_min: int = 1
    speed_max: int = 3
    speed_scale: int = 100

    avoid_range: int = 50
    avoid_factor: float = 0.4

    # align_active: bool = False
    align_range: int = 100
    align_factor: float = 0.2

    # cohesion_active: bool = False
    cohesion_range: int = 100
    cohesion_factor: float = 0.5

    # boundary_active: bool = True
    boundary_margin: int = 50
    boundary_factor: int = 10

    # cyclic_horizontal: bool = True
    # cyclic_vertical: bool = True

    # wall_horizontal: bool = False
    # wall_vertical: bool = False

    values_changed = False


def check_allowed_values(value, value_min, value_max):
    value = 0 if value in ['', '-'] else int(value)
    if value >= value_max:
        return value_max
    elif value <= value_min:
        return value_min
    else:
        return value


class UserInterface:
    def __init__(self, window, width, height, margin: int = 100, slider_range: int = 100):
        tp.init(window, tp.theme_text_dark)
        tp.TitleBox.style_normal.bottom_line = False
        tp.TitleBox.style_normal.left_line = False
        tp.TitleBox.style_normal.right_line = False

        self.WIDTH = width
        self.HEIGHT = height
        self.margin = margin
        self.window = window

        self.parameters = BoidFlockingParameters()

        self.menu_active = False
        self.updater = None

        self.slider_range = slider_range

        self.boid_number, self.boid_size = None, None
        self.boid_row, self.boid_box = None, None
        self.speed_scale, self.speed_min, self.speed_max = None, None, None
        self.speed_row, self.speed_box = None, None
        self.avoid_range, self.avoid_factor = None, None
        self.avoid_row, self.avoid_box = None, None
        self.main_box = None

        self.create_boid_widgets()
        self.create_speed_widgets()
        self.create_main_box()
        self.create_updater()

    def get_parameters(self):
        return self.parameters

    def create_boid_widgets(self):
        self.boid_number = tp.TextInput("", placeholder=f'{self.parameters.boid_number}    ')
        self.boid_number.max_length = 4
        self.boid_number.set_only_integers()
        self.boid_number.on_validation = partial(self.input_validation, self.boid_number)
        self.boid_size = tp.TextInput("", placeholder=f'{self.parameters.boid_size}    ')
        self.boid_size.max_length = 2
        self.boid_size.set_only_integers()
        self.boid_size.on_validation = partial(self.input_validation, self.boid_size)
        self.boid_row = tp.Group([tp.Text('NUMBER'), self.boid_number, tp.Text('SIZE'), self.boid_size], 'h')
        self.boid_box = tp.TitleBox('Boid', children=[self.boid_row])

    def create_speed_widgets(self):
        self.speed_scale = tp.TextInput("", placeholder=f'{self.parameters.speed_scale}    ')
        self.speed_scale.max_length = 3
        self.speed_scale.set_only_integers()
        self.speed_scale.on_validation = partial(self.input_validation, self.speed_scale)
        self.speed_min = tp.TextInput("", placeholder=f'{self.parameters.speed_min}    ')
        self.speed_min.max_length = 2
        self.speed_min.set_only_integers()
        self.speed_min.on_validation = partial(self.input_validation, self.speed_min)
        self.speed_max = tp.TextInput("", placeholder=f'{self.parameters.speed_max}    ')
        self.speed_max.max_length = 2
        self.speed_max.set_only_integers()
        self.speed_max.on_validation = partial(self.input_validation, self.speed_max)
        self.speed_row = tp.Group([tp.Text('SCALE'), self.speed_scale, tp.Text('MIN'),
                                   self.speed_min, tp.Text('MAX'), self.speed_max], 'h')
        self.speed_box = tp.TitleBox('Speed', children=[self.speed_row])

    def create_avoid_widgets(self):
        self.avoid_range = tp.TextInput("", placeholder=f'{self.parameters.avoid_range}    ')
        self.avoid_range.max_length = 3
        self.avoid_range.set_only_integers()
        self.avoid_range.on_validation = partial(self.input_validation, self.avoid_range)
        self.avoid_factor = tp.TextInput("", placeholder=f'{self.parameters.avoid_factor}    ')
        self.avoid_factor.max_length = 5
        self.avoid_factor.set_only_numbers()
        self.avoid_factor.on_validation = partial(self.input_validation, self.avoid_factor)
        self.avoid_row = tp.Group([tp.Text('RANGE'), self.avoid_range, tp.Text('FACTOR'), self.avoid_factor])
        self.avoid_box = tp.TitleBox('Separation', children=[self.avoid_row])

    def create_main_box(self):
        children = [self.boid_box, self.speed_box]
        self.main_box = tp.TitleBox('Parameters', children=children)
        self.main_box.set_topleft(self.WIDTH - self.main_box.rect.size[0] - self.margin, self.margin)

    def input_validation(self, changed_widget):
        widget_value = changed_widget.get_value()
        if changed_widget == self.boid_number:
            widget_value = check_allowed_values(widget_value, 1, 2000)
            self.parameters.boid_number = widget_value
        elif changed_widget == self.boid_size:
            widget_value = check_allowed_values(widget_value, 1, 10)
            self.parameters.boid_size = widget_value
        elif changed_widget == self.speed_scale:
            widget_value = check_allowed_values(widget_value, 10, 500)
            self.parameters.speed_scale = widget_value
        elif changed_widget == self.speed_min:
            widget_value = check_allowed_values(widget_value, 1, 10)
            self.parameters.speed_min = widget_value
        elif changed_widget == self.speed_max:
            widget_value = check_allowed_values(widget_value, 1, 10)
            self.parameters.speed_max = widget_value
        self.parameters.values_changed = True
        print(self.parameters)

    def create_updater(self):
        self.updater = self.main_box.get_updater()

    def activate_menu(self):
        self.menu_active = True

    def deactivate_menu(self):
        self.menu_active = False

    def get_menu_state(self):
        return self.menu_active

    def update(self, events, mouse_rel):
        if self.menu_active:
            self.updater.update(events=events, mouse_rel=mouse_rel)


def main():
    running = True
    pygame.init()
    WIDTH, HEIGHT = 1920, 1080
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 30
    dt = 1 / fps

    user_interface = UserInterface(window, WIDTH, HEIGHT, margin=50)
    # simulation_parameters = user_interface.get_parameters()
    # print(simulation_parameters)

    while running:
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
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            #     print(user_interface.get_parameters())
        window.fill((0, 0, 0))
        user_interface.update(events, pygame.mouse.get_rel())
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()
