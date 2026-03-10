import pybullet as p
import pybullet_data

class HumanoidEnv:

    def __init__(self):

        p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.81)

        p.loadURDF("plane.urdf")

        self.robot=p.loadURDF("models/humanoid/humanoid.urdf",[0,0,1])

    def step(self):

        p.stepSimulation()