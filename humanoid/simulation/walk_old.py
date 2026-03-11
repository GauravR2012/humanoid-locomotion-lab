import pybullet as p
import pybullet_data
import os
import time

p.connect(p.GUI)

p.setGravity(0,0,-9.81)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")

# project root
root = os.getcwd()

# model folder
model_dir = os.path.join(root,"models","humanoid")

# allow pybullet to find meshes
p.setAdditionalSearchPath(model_dir)

robot_path = os.path.join(model_dir,"nao.urdf")

print("Loading:", robot_path)

robot = p.loadURDF(
    robot_path,
    [0,0,0.35],
    flags=p.URDF_USE_SELF_COLLISION
)

print("NAO loaded successfully")

while True:
    p.stepSimulation()
    time.sleep(1/240)