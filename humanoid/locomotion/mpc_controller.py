import numpy as np

class MPCController:

    def __init__(self,horizon=20,dt=0.02):

        self.horizon=horizon
        self.dt=dt

    def optimize(self,x,v):

        traj=[]

        for _ in range(self.horizon):

            u=-0.4*x-0.1*v
            v=v+u*self.dt
            x=x+v*self.dt

            traj.append(x)

        return np.array(traj)