import cv2

from typing import Literal


class CursorRenderer:
    def __init__(self):
        self.cursor_color_rgb = (255, 255, 0)
        self.cursor_color_bgr = self.cursor_color_rgb[::-1]
        self.cursor_radius = 6
        self.cursor_thickness = 3
        self.is_animating_click = False
        self.click_color_rgb = (255, 0, 255)
        self.click_color_bgr = self.click_color_rgb[::-1]
        self.click_thickness = 3
        self.click_animation_step = 0
        self.click_animation_steps = 10
        self.click_radius_start = 12
        self.click_radius_end = 36

    def calc_mouse_relative_position(self, mouse_x, mouse_y, region_x1, region_y1):
        self.abs_mouse_x = mouse_x
        self.abs_mouse_y = mouse_y
        self.rel_mouse_x = mouse_x - region_x1
        self.rel_mouse_y = mouse_y - region_y1

    def render_cursor(self, frame):
        cv2.circle(
            frame,
            (self.rel_mouse_x, self.rel_mouse_y),
            self.cursor_radius,
            self.cursor_color_bgr,
            self.cursor_thickness,
        )

    def on_click(self):
        self.is_animating_click = True
        self.click_animation_step = 0

    def interpolate(
        self,
        a: int,
        b: int,
        t: float,
        interp_type: Literal["linear", "param"] = "linear",
        interp_param: float = 2,
    ):
        if interp_type == "param":
            new_t = t * t / (interp_param * (t * t - t) + 1)
        else:
            new_t = t

        return int(a + (b - a) * new_t)

    def calc_click_circle_radius(self):
        click_radius = self.interpolate(
            self.click_radius_start,
            self.click_radius_end,
            self.click_animation_step / self.click_animation_steps,
        )
        return click_radius

    def render_mouse_click(self, frame):
        if self.is_animating_click:
            if self.click_animation_step < self.click_animation_steps:
                self.click_animation_step += 1
                click_radius = self.calc_click_circle_radius()
                cv2.circle(
                    frame,
                    (self.rel_mouse_x, self.rel_mouse_y),
                    click_radius,
                    self.click_color_rgb,
                    self.click_thickness,
                )
            else:
                self.is_animating_click = False
                self.click_animation_step = 0

    def render(self, frame, mouse_x, mouse_y, region_x1=0, region_y1=0):
        self.calc_mouse_relative_position(mouse_x, mouse_y, region_x1, region_y1)
        self.render_cursor(frame)
        self.render_mouse_click(frame)
