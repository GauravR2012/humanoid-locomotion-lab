import numpy as np

class COMTrajectory:

    def generate(self,footsteps):

        traj=[]

        for step in footsteps:

            for _ in range(20):

                traj.append(step)

        return np.array(traj)