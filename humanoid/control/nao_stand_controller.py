import pybullet as p

class NaoStandController:

    def __init__(self, robot):
        self.robot = robot

        self.joint_ids = []
        self.joint_names = []

        for i in range(p.getNumJoints(robot)):
            info = p.getJointInfo(robot,i)
            joint_type = info[2]

            if joint_type == p.JOINT_REVOLUTE:
                self.joint_ids.append(i)
                self.joint_names.append(info[1].decode())

        # simple standing pose
        self.stand_pose = {}

        for j in self.joint_ids:
            self.stand_pose[j] = 0.0

    def step(self):

        for j in self.joint_ids:

            target = self.stand_pose[j]

            p.setJointMotorControl2(
                self.robot,
                j,
                p.POSITION_CONTROL,
                targetPosition=target,
                force=80
            )