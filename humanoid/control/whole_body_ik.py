import pybullet as p
import numpy as np


class WholeBodyIK:

    def __init__(self, robot):

        self.robot = robot
        self.num_joints = p.getNumJoints(robot)

        # store actuated joints only
        self.joint_indices = []

        for j in range(self.num_joints):

            info = p.getJointInfo(robot, j)
            joint_type = info[2]

            if joint_type == p.JOINT_REVOLUTE or joint_type == p.JOINT_PRISMATIC:
                self.joint_indices.append(j)

        self.dof = len(self.joint_indices)


    def get_joint_positions(self):

        q = []

        for j in self.joint_indices:
            q.append(p.getJointState(self.robot, j)[0])

        return np.array(q)


    def apply_joint_positions(self, q):

        for i, j in enumerate(self.joint_indices):

            p.setJointMotorControl2(
                bodyUniqueId=self.robot,
                jointIndex=j,
                controlMode=p.POSITION_CONTROL,
                targetPosition=float(q[i]),
                force=200
            )


    def solve(self, swing_link, support_link, swing_target):

        q = self.get_joint_positions()

        for _ in range(30):

            link_state = p.getLinkState(self.robot, swing_link)

            pos = np.array(link_state[0])

            error = np.array(swing_target) - pos

            if np.linalg.norm(error) < 1e-4:
                break


            zero_vec = [0.0] * self.dof

            J_lin, J_ang = p.calculateJacobian(
                bodyUniqueId=self.robot,
                linkIndex=swing_link,
                localPosition=[0, 0, 0],
                objPositions=list(q),
                objVelocities=zero_vec,
                objAccelerations=zero_vec
            )


            J_lin = np.array(J_lin)

            # remove floating base columns
            if J_lin.shape[1] > self.dof:
                J_lin = J_lin[:, -self.dof:]


            J_pinv = np.linalg.pinv(J_lin)

            dq = J_pinv @ error
            dq = np.clip(dq, -0.04, 0.04)
            q = q + dq


        return q