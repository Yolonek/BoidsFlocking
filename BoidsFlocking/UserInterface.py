import thorpy as tp


class UserInterface:
    def __init__(self, window, width, height, margin: int = 100):
        tp.init(window, tp.theme_text_dark)
        tp.TitleBox.style_normal.bottom_line = False
        tp.TitleBox.style_normal.left_line = False
        tp.TitleBox.style_normal.right_line = False
        self.WIDTH = width
        self.HEIGHT = height
        self.margin = margin
        self.window = window

        self.menu_active = False
        self.updater = None

        self.row_boid = None
        self.row_speed, self.box_speed = None, None
        self.row_avoid, self.box_avoid = None, None
        self.row_align, self.box_align = None, None
        self.row_cohesion, self.box_cohesion = None, None
        self.row_boundary, self.box_boundary = None, None
        self.row_cyclic, self.box_cyclic = None, None
        self.row_wall, self.box_wall = None, None
        self.main_box = None

        self.create_row_boid()
        self.create_row_speed()
        self.create_row_avoid()
        self.create_row_align()
        self.create_row_cohesion()
        self.create_row_boundary()
        # self.create_row_cyclic()
        # self.create_row_wall()
        self.create_main_box()
        self.create_updater()

    def create_row_boid(self):
        self.row_boid = tp.SliderWithText('Boid size', 1, 10, 5, 100)

    def create_row_speed(self):
        speed_active = tp.SwitchButtonWithText('active', texts=('', ''))
        speed_range = tp.SliderWithText('scale', 1, 10, 3, 40)
        speed_scale = tp.SliderWithText('range', 100, 500, 100, 40)
        # speed_scale.set_size((speed_scale.rect.size[0], 100))
        self.row_speed = tp.Group([speed_active, speed_range, speed_scale], 'h')
        self.box_speed = tp.TitleBox('Speed', children=[self.row_speed])

    def create_row_avoid(self):
        avoid_active = tp.SwitchButtonWithText('active', texts=('', ''))
        avoid_range = tp.SliderWithText('range', 10, 200, 50, 40)
        avoid_factor = tp.SliderWithText('factor', 0, 2, 0.4, 40)
        self.row_avoid = tp.Group([avoid_active, avoid_range, avoid_factor], 'h')
        self.box_avoid = tp.TitleBox('Avoidance', children=[self.row_avoid])

    def create_row_align(self):
        align_active = tp.SwitchButtonWithText('active', texts=('', ''))
        align_range = tp.SliderWithText('range', 10, 500, 50, 40)
        align_factor = tp.SliderWithText('factor', 0, 2, 0.4, 40)
        self.row_align = tp.Group([align_active, align_range, align_factor], 'h')
        self.box_align = tp.TitleBox('Alignment', children=[self.row_align])

    def create_row_cohesion(self):
        cohesion_active = tp.SwitchButtonWithText('active', texts=('', ''))
        cohesion_range = tp.SliderWithText('range', 10, 500, 50, 40)
        cohesion_factor = tp.SliderWithText('factor', 0, 2, 0.4, 40)
        self.row_cohesion = tp.Group([cohesion_active, cohesion_range, cohesion_factor], 'h')
        self.box_cohesion = tp.TitleBox('Cohesion', children=[self.row_cohesion])

    def create_row_boundary(self):
        boundary_active = tp.SwitchButtonWithText('active', texts=('', ''))
        boundary_margin = tp.SliderWithText('margin', 10, 500, 50, 40)
        boundary_factor = tp.SliderWithText('factor', 2, 100, 0.4, 40)
        self.row_boundary = tp.Group([boundary_active, boundary_margin, boundary_factor], 'h')
        self.create_row_cyclic()
        self.create_row_wall()
        self.box_boundary = tp.TitleBox('Boundaries', children=[self.row_boundary, self.box_cyclic, self.box_wall])

    def create_row_cyclic(self):
        cyclic_horizontal = tp.SwitchButtonWithText('Horizontal', texts=('on', 'off'))
        cyclic_vertical = tp.SwitchButtonWithText('Vertical', texts=('on', 'off'))
        self.row_cyclic = tp.Group([cyclic_horizontal, cyclic_vertical], 'h')
        self.box_cyclic = tp.TitleBox('Cyclic', children=[self.row_cyclic])

    def create_row_wall(self):
        wall_horizontal = tp.SwitchButtonWithText('Horizontal', texts=('on', 'off'))
        wall_vertical = tp.SwitchButtonWithText('Vertical', texts=('on', 'off'))
        self.row_wall = tp.Group([wall_horizontal, wall_vertical], 'h')
        self.box_wall = tp.TitleBox('Wall', children=[self.row_wall])

    def create_main_box(self):
        children = [self.row_boid, self.box_speed, self.box_avoid, self.box_align, self.box_cohesion, self.box_boundary]
        self.main_box = tp.TitleBox('Parameters', children=children)
        self.main_box.set_topleft(self.WIDTH - self.main_box.rect.size[0] - self.margin, self.margin)

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
