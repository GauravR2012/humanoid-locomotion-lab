import matplotlib.pyplot as plt

from humanoid.locomotion.lipm_dynamics import LIPMDynamics

lipm=LIPMDynamics()

x=0
v=0.3
dt=0.02

traj=[]

for _ in range(300):

    x,v=lipm.step(x,v,dt)
    traj.append(x)

plt.plot(traj)
plt.title("LIPM Stability")

plt.savefig("results/plots/lipm.png")