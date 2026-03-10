import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# -----------------------
# Parameters
# -----------------------

g = 9.81
h = 0.8
omega = np.sqrt(g/h)

dt = 0.02
T = 3

# Output folders
frames_dir = "results/frames"
gif_path = "results/gifs/walking.gif"

os.makedirs(frames_dir, exist_ok=True)
os.makedirs("results/gifs", exist_ok=True)

# -----------------------
# LIPM Dynamics
# -----------------------

x = 0
v = 0.4

traj = []

for i in range(int(T/dt)):

    x_new = x*np.cosh(omega*dt) + (v/omega)*np.sinh(omega*dt)
    v_new = x*omega*np.sinh(omega*dt) + v*np.cosh(omega*dt)

    x, v = x_new, v_new
    traj.append(x)

traj = np.array(traj)

# -----------------------
# Generate Frames
# -----------------------

frames = []

for i in range(len(traj)):

    plt.figure(figsize=(6,4))

    plt.plot(traj[:i], label="CoM trajectory")
    plt.scatter(i, traj[i])

    plt.xlabel("Time Step")
    plt.ylabel("Center of Mass Position")
    plt.title("Humanoid CoM Dynamics (LIPM)")
    plt.legend()

    frame_path = os.path.join(frames_dir, f"frame_{i:03d}.png")

    plt.savefig(frame_path)
    plt.close()

    frames.append(imageio.imread(frame_path))

# -----------------------
# Create GIF
# -----------------------

imageio.mimsave(gif_path, frames, duration=0.05)

print("Frames saved in:", frames_dir)
print("GIF saved at:", gif_path)