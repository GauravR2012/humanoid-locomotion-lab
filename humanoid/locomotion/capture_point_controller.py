import numpy as np


class CapturePointController:

    def __init__(self, com_height, g=9.81):

        self.omega = np.sqrt(g / com_height)


    def compute(self, com_pos, com_vel):

        """
        Capture point:
        cp = x + x_dot / omega
        """

        return com_pos + com_vel / self.omega