from typing import Literal


class FocusRegionUpdater:
    def __init__(self, window_width=1280, window_height=720):
        self.focus_x, self.focus_y = 0, 0
        self.move_start_x, self.move_start_y = 0, 0
        self.window_width = window_width
        self.window_height = window_height
        self.tolerance_width = min(self.window_width // 2, 600)
        self.tolerance_height = min(self.window_height // 2, 300)
        self.is_moving_x = False
        self.is_moving_y = False
        self.MOVING_X_STEPS = 30
        self.MOVING_Y_STEPS = 30
        self.moving_x_step = 0
        self.moving_y_step = 0

    def interpolate(
        self,
        a: int,
        b: int,
        t: float,
        interp_type: Literal["linear", "param"] = "param",
        interp_param: float = 2,
    ):
        if interp_type == "param":
            new_t = t * t / (interp_param * (t * t - t) + 1)
        else:
            new_t = t

        return int(a + (b - a) * new_t)

    def calc_focus_center(self, mouse_x, mouse_y):
        """calculate center of focus region based on current and previous mouse position"""
        if self.is_moving_x:
            self.moving_x_step += 1
            if self.moving_x_step > self.MOVING_X_STEPS:
                self.is_moving_x = False
                self.moving_x_step = 0
            else:
                self.focus_x = self.interpolate(
                    self.move_start_x, mouse_x, self.moving_x_step / self.MOVING_X_STEPS
                )
        else:
            if abs(mouse_x - self.move_start_x) > self.tolerance_width:
                self.move_start_x = self.focus_x
                self.is_moving_x = True

        if self.is_moving_y:
            self.moving_y_step += 1
            if self.moving_y_step > self.MOVING_Y_STEPS:
                self.is_moving_y = False
                self.moving_y_step = 0
            else:
                self.focus_y = self.interpolate(
                    self.move_start_y, mouse_y, self.moving_y_step / self.MOVING_Y_STEPS
                )
        else:
            if abs(mouse_y - self.move_start_y) > self.tolerance_height:
                self.move_start_y = self.focus_y
                self.is_moving_y = True

        return self.focus_x, self.focus_y
