import numpy as np
import cv2
from mss import mss


class MainApp:
    def __init__(self):
        self.window_name = "Mouse-Screen"
        self.window_width = 1280
        self.window_height = 720
        self.setup_window()

    def setup_window(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)

    def detect_mouse_position(self):
        pass

    def run(self):
        # use mss to capture screen, and use cv2 to real-time display each frame
        with mss() as sct:
            while True:
                frame = sct.grab(sct.monitors[1])
                frame_img = np.array(frame)
                cv2.imshow(self.window_name, frame_img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    app = MainApp()
    app.run()

    # python -m apps.app
