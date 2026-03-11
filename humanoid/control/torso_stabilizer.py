import pybullet as p


class TorsoStabilizer:

    def __init__(self, robot):

        self.robot = robot

        self.kp = 0.4


    def stabilize(self):

        pos, orn = p.getBasePositionAndOrientation(self.robot)

        euler = p.getEulerFromQuaternion(orn)

        roll = euler[0]
        pitch = euler[1]

        correction_roll = -self.kp * roll
        correction_pitch = -self.kp * pitch

        new_orn = p.getQuaternionFromEuler(
            [correction_roll, correction_pitch, 0]
        )

        p.resetBasePositionAndOrientation(self.robot, pos, new_orn)