import numpy as np

class CapturePoint:

    def __init__(self,com_height=0.8,gravity=9.81):

        self.omega=np.sqrt(gravity/com_height)

    def compute(self,pos,vel):

        return pos+vel/self.omega