import numpy as np

class FootstepPlanner:

    def __init__(self, step_length=0.15, step_width=0.1):
        self.step_length = step_length
        self.step_width = step_width

    def generate_zmp_trajectory(steps, step_time, dt):

        zmp = []

        samples = int(step_time / dt)

        for step in steps:

            for _ in range(samples):
                zmp.append(step["pos"][0])

        return np.array(zmp)

    def generate(self, n_steps):

        steps = []

        for i in range(n_steps):

            x = i * self.step_length

            if i % 2 == 0:
                y = self.step_width
                foot = "left"
            else:
                y = -self.step_width
                foot = "right"

            steps.append(
                {
                    "foot": foot,
                    "pos": np.array([x, y])
                }
            )

        return steps