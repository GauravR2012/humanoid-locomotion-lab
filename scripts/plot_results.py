import numpy as np
import matplotlib.pyplot as plt

com = np.load("results/data/com.npy")

plt.plot(com[:,0], label="COM X")
plt.plot(com[:,1], label="COM Y")

plt.legend()
plt.title("Center of Mass Trajectory")

plt.savefig("results/com_plot.png")