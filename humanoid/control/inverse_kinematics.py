import numpy as np

class LegIK:

    def solve(self,foot_pos):

        hip=np.arctan2(foot_pos[1],foot_pos[0])
        knee=np.linalg.norm(foot_pos)
        ankle=-hip

        return hip,knee,ankle