import pybullet as p

class NaoController:

    def __init__(self, robot):

        self.robot = robot
        self.joints = []

        for i in range(p.getNumJoints(robot)):

            info = p.getJointInfo(robot, i)

            if info[2] == p.JOINT_REVOLUTE:
                self.joints.append(i)

    def apply(self, joint_targets):

        # Apply targets only for valid indices
        for i, joint_id in enumerate(self.joints):

            if i >= len(joint_targets):
                break

            p.setJointMotorControl2(
                self.robot,
                joint_id,
                p.POSITION_CONTROL,
                targetPosition=joint_targets[i],
                force=100
            )