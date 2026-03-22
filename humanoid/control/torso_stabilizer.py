import pybullet as p


class TorsoStabilizer:

    def __init__(self, robot):

        self.robot = robot

        self.kp_roll = 0.6
        self.kp_pitch = 0.6


    def stabilize(self):

        pos, orn = p.getBasePositionAndOrientation(self.robot)

        roll,pitch,yaw = p.getEulerFromQuaternion(orn)

        correction_roll = -self.kp_roll * roll
        correction_pitch = -self.kp_pitch * pitch

        new_orn = p.getQuaternionFromEuler(
            [correction_roll, correction_pitch, yaw]
        )

        p.resetBasePositionAndOrientation(
            self.robot,
            pos,
            new_orn
        )