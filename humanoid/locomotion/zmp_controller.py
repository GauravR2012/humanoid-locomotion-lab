import numpy as np

class ZMPController:

    def __init__(self,com_height=0.8,gravity=9.81):

        self.h=com_height
        self.g=gravity

    def compute(self,com_pos,com_acc):

        px=com_pos[0]-(self.h/self.g)*com_acc[0]
        py=com_pos[1]-(self.h/self.g)*com_acc[1]

        return np.array([px,py])