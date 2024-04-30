import cv2


class CursorRenderer:
    def __init__(self):
        self.cursor_color_rgb = (255, 255, 0)
        self.cursor_color_bgr = self.cursor_color_rgb[::-1]
        self.cursor_radius = 6
        self.cursor_thickness = 3

    def render(self, frame, mouse_x, mouse_y, region_x1=0, region_y1=0):
        x = mouse_x - region_x1
        y = mouse_y - region_y1
        cv2.circle(
            frame,
            (x, y),
            self.cursor_radius,
            self.cursor_color_bgr,
            self.cursor_thickness,
        )
