import cv2
import numpy as np

from mss import mss
from pynput import mouse
from tclogger import logger


class MainApp:
    def __init__(self):
        self.window_name = "Mouse-Screen"
        self.window_width, self.window_height = 1280, 720
        self.mouse_x, self.mouse_y = 0, 0
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)

    def on_mouse_move(self, x, y):
        self.mouse_x, self.mouse_y = x, y

    def detect_active_monitor(self):
        """detect active monitor, where the mouse is currently located"""
        self.active_monitor = None
        for idx, monitor in enumerate(self.monitors[1:]):
            if (
                self.mouse_x >= monitor["left"]
                and self.mouse_x <= monitor["left"] + monitor["width"]
                and self.mouse_y >= monitor["top"]
                and self.mouse_y <= monitor["top"] + monitor["height"]
            ):
                self.active_monitor = monitor
                break
        if self.active_monitor is None:
            self.active_monitor = self.monitors[0]

    def calc_mouse_region(self):
        """calculate the region of the screen to capture based on the mouse position"""
        self.region_top_left_x = self.mouse_x - self.window_width // 2
        self.region_top_left_y = self.mouse_y - self.window_height // 2
        self.region_bottom_right_x = self.mouse_x + self.window_width // 2
        self.region_bottom_right_y = self.mouse_y + self.window_height // 2
        self.mouse_region = {
            "top": self.region_top_left_y,
            "left": self.region_top_left_x,
            "width": self.region_bottom_right_x - self.region_top_left_x,
            "height": self.region_bottom_right_y - self.region_top_left_y,
        }

    def run(self):
        """use mss to capture screen, and use cv2 to real-time display each frame"""
        with mss() as sct:
            self.monitors = sct.monitors
            with mouse.Listener(on_move=self.on_mouse_move) as listener:
                while True:
                    self.detect_active_monitor()
                    self.calc_mouse_region()
                    frame = sct.grab(self.mouse_region)
                    frame_np = np.array(frame)
                    cv2.imshow(self.window_name, frame_np)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        cv2.destroyAllWindows()
                        break


if __name__ == "__main__":
    app = MainApp()
    app.run()

    # python -m apps.app
