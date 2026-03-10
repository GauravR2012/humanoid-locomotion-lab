import numpy as np

class PreviewController:

    def __init__(self,horizon=100,dt=0.02):

        self.horizon=horizon
        self.dt=dt

    def compute(self,zmp_ref):

        x=0
        v=0

        traj=[]

        for i in range(self.horizon):

            u=zmp_ref[i]-x

            v+=u*self.dt
            x+=v*self.dt

            traj.append(x)

        return np.array(traj)