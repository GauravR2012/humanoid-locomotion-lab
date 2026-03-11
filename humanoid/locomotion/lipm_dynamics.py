import numpy as np

class LIPMDynamics:

    def __init__(self, com_height=0.35, g=9.81):

        self.h = com_height
        self.g = g

        self.omega = np.sqrt(g / com_height)

    def step(self, x, v, zmp, dt):

        x_ddot = self.omega**2 * (x - zmp)

        v = v + x_ddot * dt
        x = x + v * dt

        return x, v