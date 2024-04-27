import numpy as np
import cv2
from mss import mss


class MainApp:
    def __init__(self):
        pass

    def run(self):
        # use mss to capture screen, and use cv2 to real-time display each frame
        with mss() as sct:
            while True:
                frame = sct.grab(sct.monitors[1])
                frame_np = np.array(frame)
                frame_img = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
                cv2.imshow("frame", frame_img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break


if __name__ == "__main__":
    app = MainApp()
    app.run()

    # python -m apps.app
