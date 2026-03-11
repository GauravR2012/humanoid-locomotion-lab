import numpy as np


class SwingFootTrajectory:

    def __init__(self, step_height=0.05):

        self.step_height = step_height


    def generate(self, start, end, phase):

        phase = np.clip(phase,0,1)

        # smooth cubic interpolation
        s = 3*phase**2 - 2*phase**3

        x = start[0] + (end[0] - start[0]) * s
        y = start[1] + (end[1] - start[1]) * s

        z = self.step_height * np.sin(np.pi * phase)

        return [x,y,z]