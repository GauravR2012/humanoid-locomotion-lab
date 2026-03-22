import pybullet as p
import numpy as np


class PelvisTrajectory:

    def __init__(self, robot, height=0.35):

        self.robot = robot
        self.height = height

        self.kp = 0.12


    def update(self, com_x, com_y):

        pos, orn = p.getBasePositionAndOrientation(self.robot)

        x = pos[0]
        y = pos[1]
        z = pos[2]

        x = x + self.kp * (com_x - x)
        y = y + self.kp * (com_y - y)

        z = self.height

        p.resetBasePositionAndOrientation(
            self.robot,
            [x, y, z],
            orn
        )

        return [x, y, z]