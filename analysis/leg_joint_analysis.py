import numpy as np
import matplotlib.pyplot as plt


data = np.load("results/data/joints.npy")

# NAO leg joints indices
LHipYawPitch = 13
LHipRoll = 14
LHipPitch = 15
LKneePitch = 16
LAnklePitch = 17
LAnkleRoll = 18

RHipYawPitch = 26
RHipRoll = 27
RHipPitch = 28
RKneePitch = 29
RAnklePitch = 30
RAnkleRoll = 31


left_leg = [
    LHipYawPitch,
    LHipRoll,
    LHipPitch,
    LKneePitch,
    LAnklePitch,
    LAnkleRoll
]

right_leg = [
    RHipYawPitch,
    RHipRoll,
    RHipPitch,
    RKneePitch,
    RAnklePitch,
    RAnkleRoll
]


names = [
    "HipYawPitch",
    "HipRoll",
    "HipPitch",
    "KneePitch",
    "AnklePitch",
    "AnkleRoll"
]


for i in range(6):

    plt.figure()

    plt.plot(data[:,left_leg[i]], label="Left")

    plt.plot(data[:,right_leg[i]], label="Right")

    plt.title(names[i])

    plt.xlabel("Time")

    plt.ylabel("Angle")

    plt.legend()

    plt.grid(True)

    plt.show()