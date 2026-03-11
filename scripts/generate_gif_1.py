import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# ---------------------------
# Parameters
# ---------------------------

step_length = 0.25
step_width = 0.18
num_steps = 12
dt = 0.05

frames_dir = "results/frames"
gif_path = "results/gifs/walking.gif"

os.makedirs(frames_dir, exist_ok=True)
os.makedirs("results/gifs", exist_ok=True)

# ---------------------------
# Footstep Planning
# ---------------------------

footsteps = []

for i in range(num_steps):

    x = i * step_length
    y = step_width if i % 2 == 0 else -step_width

    footsteps.append((x, y))

footsteps = np.array(footsteps)

# ---------------------------
# CoM Trajectory
# ---------------------------

com_traj = []

for i in range(len(footsteps)-1):

    start = footsteps[i]
    end = footsteps[i+1]

    for t in np.linspace(0,1,15):

        x = (1-t)*start[0] + t*end[0]
        y = (1-t)*start[1] + t*end[1]

        com_traj.append((x,y))

com_traj = np.array(com_traj)

# ---------------------------
# Generate Frames
# ---------------------------

frames = []

for i in range(len(com_traj)):

    plt.figure(figsize=(6,4))

    # footsteps
    left = footsteps[::2]
    right = footsteps[1::2]

    plt.scatter(left[:,0], left[:,1], label="Left Foot")
    plt.scatter(right[:,0], right[:,1], label="Right Foot")

    # CoM trajectory
    plt.plot(com_traj[:i,0], com_traj[:i,1], label="CoM Path")

    plt.scatter(com_traj[i,0], com_traj[i,1], label="CoM")

    plt.xlabel("Forward Motion")
    plt.ylabel("Lateral Motion")

    plt.title("Humanoid Walking Trajectory")

    plt.legend()
    plt.axis("equal")

    frame_path = os.path.join(frames_dir, f"frame_{i:03d}.png")

    plt.savefig(frame_path)
    plt.close()

    frames.append(imageio.imread(frame_path))

# ---------------------------
# Create GIF
# ---------------------------

imageio.mimsave(gif_path, frames, duration=0.07)

print("Frames saved in:", frames_dir)
print("GIF saved at:", gif_path)