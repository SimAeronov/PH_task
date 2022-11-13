"""
Note: I use pynput as it should work both with Windows and Linux
"""
from pynput.mouse import Listener, Button


class MouseListener:
    """
    This class is used to record mouse coordinates as well as to listen for LMB click.
    Mouse coordinates are saved in self.coord_X and self.coord_Y
    Upon LMB click, self.cv_photo -> True, else False
    """

    def on_move(self, x, y):
        self.coord_X = int(x)
        self.coord_Y = int(y)

    def on_click(self, x, y, button, pressed):
        if button == Button.left and pressed:
            self.cv_photo = True

    def __init__(self):
        self.coord_X = 0
        self.coord_Y = 0
        self.cv_photo = False

        self.listener = Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.listener.start()


    @classmethod
    def stop_listening(cls):
        cls.listener.stop()
