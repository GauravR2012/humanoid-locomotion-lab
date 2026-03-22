import numpy as np
import matplotlib.pyplot as plt
import pybullet as p
import pybullet_data
import os


# ----------------------------
# Load joint data
# ----------------------------

data = np.load("results/data/joints.npy")

steps, joints = data.shape

print("Timesteps:", steps)
print("Joints:", joints)


# ----------------------------
# Load robot to get names
# ----------------------------

p.connect(p.DIRECT)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

robot = p.loadURDF(
    "models/humanoid/nao.urdf",
    [0,0,0.35]
)

joint_names = []

for i in range(p.getNumJoints(robot)):

    info = p.getJointInfo(robot,i)

    name = info[1].decode()

    joint_names.append(name)

p.disconnect()


# ----------------------------
# Create folder
# ----------------------------

os.makedirs("results/plots/joints", exist_ok=True)


# ----------------------------
# Plot each joint
# ----------------------------

for j in range(joints):

    plt.figure()

    plt.plot(data[:,j])

    if j < len(joint_names):
        title = joint_names[j]
    else:
        title = f"Joint {j}"

    plt.title(title)

    plt.xlabel("Time step")

    plt.ylabel("Joint angle (rad)")

    plt.grid(True)

    plt.savefig(f"results/plots/joints/joint_{j}.png")

    plt.close()


print("Joint plots saved to results/plots/joints")