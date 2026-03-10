import numpy as np

class LIPMDynamics:

    def __init__(self,com_height=0.8,gravity=9.81):

        self.h=com_height
        self.g=gravity
        self.omega=np.sqrt(self.g/self.h)

    def step(self,x,v,dt):

        x_new=x*np.cosh(self.omega*dt)+(v/self.omega)*np.sinh(self.omega*dt)
        v_new=x*self.omega*np.sinh(self.omega*dt)+v*np.cosh(self.omega*dt)

        return x_new,v_new