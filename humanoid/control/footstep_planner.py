import numpy as np


class FootstepPlanner:

    def __init__(self, step_length=0.12, step_width=0.12):

        self.step_length = step_length
        self.step_width = step_width


    def generate(self, n_steps):

        steps = []

        x = 0

        for i in range(n_steps):

            x += self.step_length

            if i % 2 == 0:

                foot = "left"
                y = self.step_width

            else:

                foot = "right"
                y = -self.step_width


            steps.append({
                "foot": foot,
                "pos": np.array([x, y])
            })


        return steps