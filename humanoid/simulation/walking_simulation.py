
import pybullet as p
import pybullet_data
import os
import time
import numpy as np
import imageio

from humanoid.control.footstep_planner import FootstepPlanner
from humanoid.control.trajectory_generator import SwingFootTrajectory
from humanoid.control.whole_body_ik import WholeBodyIK
from humanoid.control.nao_controller import NaoController
from humanoid.locomotion.zmp_preview_controller import ZMPPreviewController
from humanoid.locomotion.capture_point_controller import CapturePointController
from humanoid.control.torso_stabilizer import TorsoStabilizer


# --------------------------------------------------
# Result folders
# --------------------------------------------------

os.makedirs("results/data", exist_ok=True)
os.makedirs("results/frames", exist_ok=True)
os.makedirs("results/plots", exist_ok=True)


# --------------------------------------------------
# Physics setup
# --------------------------------------------------

p.connect(p.GUI)
p.setGravity(0,0,-9.81)
p.setRealTimeSimulation(0)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")


# --------------------------------------------------
# Load robot
# --------------------------------------------------

model_dir = os.path.join(os.getcwd(),"models","humanoid")
p.setAdditionalSearchPath(model_dir)

robot = p.loadURDF(
    os.path.join(model_dir,"nao.urdf"),
    [0,0,0.35],
    flags=p.URDF_USE_SELF_COLLISION
)


# --------------------------------------------------
# Print joints
# --------------------------------------------------

print("\nJOINT LIST\n")

for i in range(p.getNumJoints(robot)):
    info = p.getJointInfo(robot,i)
    print(i,info[1].decode())


# --------------------------------------------------
# Important joints
# --------------------------------------------------

LEFT_FOOT = 19
RIGHT_FOOT = 32

LHIPYAWPITCH = 13
LHIPROLL = 14
LHIPPITCH = 15
LKNEEPITCH = 16
LANKLEPITCH = 17
LANKLEROLL = 18

RHIPYAWPITCH = 26
RHIPROLL = 27
RHIPPITCH = 28
RKNEEPITCH = 29
RANKLEPITCH = 30
RANKLEROLL = 31


# Prevent leg crossing
p.setJointMotorControl2(robot, LHIPYAWPITCH, p.POSITION_CONTROL, targetPosition=0, force=50)
p.setJointMotorControl2(robot, RHIPYAWPITCH, p.POSITION_CONTROL, targetPosition=0, force=50)


# --------------------------------------------------
# Controllers
# --------------------------------------------------

planner = FootstepPlanner(step_length=0.08, step_width=0.10)
steps_list = planner.generate(20)

swing = SwingFootTrajectory()
ik = WholeBodyIK(robot)
controller = NaoController(robot)
torso = TorsoStabilizer(robot)


# --------------------------------------------------
# ZMP Preview Controllers
# --------------------------------------------------

dt = 1/240

preview_x = ZMPPreviewController(
    dt=dt,
    com_height=0.35,
    preview_time=1.6
)

preview_y = ZMPPreviewController(
    dt=dt,
    com_height=0.35,
    preview_time=1.6
)

capture = CapturePointController(com_height=0.35)


# --------------------------------------------------
# Generate ZMP reference
# --------------------------------------------------

def generate_zmp(steps):

    zmp_x = []
    zmp_y = []

    samples = int(0.8/dt)

    for i,step in enumerate(steps):

        support_y = 0.05 if i % 2 == 0 else -0.05

        for _ in range(samples):

            zmp_x.append(step["pos"][0] + 0.02)
            zmp_y.append(support_y)

    return np.array(zmp_x), np.array(zmp_y)


zmp_ref_x, zmp_ref_y = generate_zmp(steps_list)


# --------------------------------------------------
# Logging
# --------------------------------------------------

com_log = []
joint_log = []
zmp_log = []

frame_id = 0


# --------------------------------------------------
# Simulation parameters
# --------------------------------------------------

SIM_TIME = 20
steps = int(SIM_TIME/dt)

phase = 0
step_index = 0


# --------------------------------------------------
# Track foot positions
# --------------------------------------------------

left_foot_pos = [0,0.06,0]
right_foot_pos = [0,-0.06,0]


print("\nWalking simulation started\n")


try:

    for t in range(steps):

        # ----------------------------------
        # ZMP preview
        # ----------------------------------

        com_x, vx, zmp_x = preview_x.step(zmp_ref_x[t:])
        com_y, vy, zmp_y = preview_y.step(zmp_ref_y[t:])


        # ----------------------------------
        # Capture point
        # ----------------------------------

        cp_x = capture.compute(com_x,vx)
        cp_y = capture.compute(com_y,vy)


        pos,_ = p.getBasePositionAndOrientation(robot)


        # ----------------------------------
        # Hip strategy (balance)
        # ----------------------------------

        lean_gain = 3.0
        desired_roll = lean_gain * (cp_y - pos[1])

        p.setJointMotorControl2(
            robot,
            LHIPROLL,
            p.POSITION_CONTROL,
            targetPosition=desired_roll,
            force=80
        )

        p.setJointMotorControl2(
            robot,
            RHIPROLL,
            p.POSITION_CONTROL,
            targetPosition=-desired_roll,
            force=80
        )


        # ----------------------------------
        # Step phase
        # ----------------------------------

        step = steps_list[step_index]

        phase += dt*0.9

        if phase >= 1:

            phase = 0
            step_index = (step_index + 1) % len(steps_list)


        # ----------------------------------
        # Determine swing leg
        # ----------------------------------

        if step_index % 2 == 0:

            swing_leg = LEFT_FOOT
            start = left_foot_pos

            p.setJointMotorControl2(robot, RHIPPITCH, p.POSITION_CONTROL, targetPosition=-0.6, force=80)
            p.setJointMotorControl2(robot, RKNEEPITCH, p.POSITION_CONTROL, targetPosition=0.4, force=80)

        else:

            swing_leg = RIGHT_FOOT
            start = right_foot_pos

            p.setJointMotorControl2(robot, LHIPPITCH, p.POSITION_CONTROL, targetPosition=-0.6, force=80)
            p.setJointMotorControl2(robot, LKNEEPITCH, p.POSITION_CONTROL, targetPosition=0.4, force=80)


        # ----------------------------------
        # Swing trajectory
        # ----------------------------------

        end = [
            step["pos"][0],
            step["pos"][1],
            0
        ]

        swing_pos = swing.generate(start,end,phase)


        # Prevent leg crossing
        min_sep = 0.07

        if swing_leg == LEFT_FOOT:
            swing_pos[1] = max(swing_pos[1],min_sep)
        else:
            swing_pos[1] = min(swing_pos[1],-min_sep)


        target = [
            swing_pos[0],
            swing_pos[1],
            swing_pos[2]
        ]


        # ----------------------------------
        # IK
        # ----------------------------------

        q = ik.solve(
                swing_link=swing_leg,
                support_link=None,
                swing_target=target
        )

        ik.apply_joint_positions(q)


        # ----------------------------------
        # Ankle strategy
        # ----------------------------------

        ankle_gain = 1.5
        ankle_correction = ankle_gain * (cp_y - pos[1])

        p.setJointMotorControl2(robot, LANKLEROLL, p.POSITION_CONTROL, targetPosition=ankle_correction, force=40)
        p.setJointMotorControl2(robot, RANKLEROLL, p.POSITION_CONTROL, targetPosition=-ankle_correction, force=40)


        # ----------------------------------
        # Update foot positions
        # ----------------------------------

        if phase >= 0.99:

            if swing_leg == LEFT_FOOT:
                left_foot_pos = end
            else:
                right_foot_pos = end


        # ----------------------------------
        # Torso stabilization
        # ----------------------------------

        torso.stabilize()


        # ----------------------------------
        # Physics
        # ----------------------------------

        p.stepSimulation()
        time.sleep(dt)


        # ----------------------------------
        # Logging
        # ----------------------------------

        pos,_ = p.getBasePositionAndOrientation(robot)

        com_log.append(pos)
        zmp_log.append([zmp_x,zmp_y])


        joint_state = []

        for j in range(p.getNumJoints(robot)):
            joint_state.append(p.getJointState(robot,j)[0])

        joint_log.append(joint_state)


        # ----------------------------------
        # Save frame
        # ----------------------------------

        width,height,img,_,_ = p.getCameraImage(640,480)

        frame = np.reshape(img,(height,width,4))[:,:,:3]
        frame = frame.astype(np.uint8)

        imageio.imwrite(
            f"results/frames/frame_{frame_id:04d}.png",
            frame
        )

        frame_id += 1


except KeyboardInterrupt:

    print("\nSimulation interrupted")


finally:

    print("\nSaving results...")

    np.save("results/data/com.npy",np.array(com_log))
    np.save("results/data/zmp.npy",np.array(zmp_log))
    np.save("results/data/joints.npy",np.array(joint_log))

    print("Results saved to results/data")

    p.disconnect()
