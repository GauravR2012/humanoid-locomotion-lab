import pybullet as p

class HumanoidIK:

    def __init__(self, robot):

        self.robot = robot

    def solve(self, link_id, target):

        joints = p.calculateInverseKinematics(
            self.robot,
            link_id,
            targetPosition=target
        )

        return joints