import time

from humanoid.simulation.pybullet_env import HumanoidEnv
from humanoid.control.footstep_planner import FootstepPlanner

env=HumanoidEnv()

planner=FootstepPlanner()

steps=planner.plan(10)

print("Footsteps:",steps)

for _ in range(2000):

    env.step()
    time.sleep(1/240)