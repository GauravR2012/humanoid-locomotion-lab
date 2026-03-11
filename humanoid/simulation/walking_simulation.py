import pybullet as p
import pybullet_data
import os
import time
import numpy as np
import imageio

from humanoid.control.footstep_planner import FootstepPlanner
from humanoid.control.trajectory_generator import SwingFootTrajectory
from humanoid.control.inverse_kinematics import HumanoidIK
from humanoid.control.nao_controller import NaoController
from humanoid.locomotion.zmp_preview_controller import ZMPPreviewController
from humanoid.locomotion.capture_point_controller import CapturePointController
from humanoid.control.torso_stabilizer import TorsoStabilizer


os.makedirs("results/data", exist_ok=True)
os.makedirs("results/frames", exist_ok=True)
os.makedirs("results/plots", exist_ok=True)


p.connect(p.GUI)
p.setGravity(0,0,-9.81)
p.setRealTimeSimulation(0)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")


model_dir = os.path.join(os.getcwd(),"models","humanoid")
p.setAdditionalSearchPath(model_dir)

robot = p.loadURDF(
    os.path.join(model_dir,"nao.urdf"),
    [0,0,0.35],
    flags=p.URDF_USE_SELF_COLLISION
)


print("\nJOINT LIST\n")

for i in range(p.getNumJoints(robot)):
    info = p.getJointInfo(robot,i)
    print(i,info[1].decode())


LEFT_FOOT = 19
RIGHT_FOOT = 32


planner = FootstepPlanner()
steps_list = planner.generate(20)

swing = SwingFootTrajectory()
ik = HumanoidIK(robot)
controller = NaoController(robot)
torso = TorsoStabilizer(robot)


dt = 1/240

preview = ZMPPreviewController(
    dt=dt,
    com_height=0.35,
    preview_time=1.6
)

capture = CapturePointController(com_height=0.35)


# --------------------------------------------------
# Generate ZMP trajectory with lateral sway
# --------------------------------------------------

def generate_zmp(steps):

    zmp = []

    for i,s in enumerate(steps):

        for _ in range(int(0.8/dt)):

            if i % 2 == 0:
                zmp.append(s["pos"][0] + 0.03)
            else:
                zmp.append(s["pos"][0] - 0.03)

    return np.array(zmp)


zmp_ref = generate_zmp(steps_list)


com_log = []
joint_log = []
zmp_log = []

frame_id = 0


SIM_TIME = 20
steps = int(SIM_TIME/dt)

phase = 0
step_index = 0


# Track foot positions
left_foot_pos = [0,0.05,0]
right_foot_pos = [0,-0.05,0]


print("\nWalking simulation started\n")


try:

    com_x = 0
    com_v = 0

    for t in range(steps):

        com_x,com_v,zmp = preview.step(zmp_ref[t:])

        cp = capture.compute(com_x,com_v)

        step = steps_list[step_index]

        phase += dt * 1.5

        if phase >= 1:

            phase = 0
            step_index = (step_index+1) % len(steps_list)


        if step_index % 2 == 0:

            swing_leg = LEFT_FOOT
            start = left_foot_pos

        else:

            swing_leg = RIGHT_FOOT
            start = right_foot_pos


        end = [step["pos"][0],step["pos"][1],0]

        swing_pos = swing.generate(start,end,phase)

        target = [
            cp + swing_pos[0],
            swing_pos[1],
            swing_pos[2]
        ]

        joints = ik.solve(swing_leg,target)
        controller.apply(joints)


        if phase >= 0.99:

            if swing_leg == LEFT_FOOT:
                left_foot_pos = end
            else:
                right_foot_pos = end


        torso.stabilize()

        p.stepSimulation()
        time.sleep(dt)


        pos,_ = p.getBasePositionAndOrientation(robot)
        com_log.append(pos)
        zmp_log.append(zmp)


        joint_state = []

        for j in range(p.getNumJoints(robot)):
            joint_state.append(p.getJointState(robot,j)[0])

        joint_log.append(joint_state)


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