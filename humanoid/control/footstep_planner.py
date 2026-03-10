import numpy as np

class FootstepPlanner:

    def __init__(self,step_length=0.25,step_width=0.2):

        self.step_length=step_length
        self.step_width=step_width

    def plan(self,n):

        steps=[]

        for i in range(n):

            x=i*self.step_length
            y=self.step_width if i%2==0 else -self.step_width

            steps.append([x,y])

        return np.array(steps)