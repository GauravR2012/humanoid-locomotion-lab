import imageio
import numpy as np
import matplotlib.pyplot as plt

frames=[]

for i in range(40):

    x=np.linspace(0,10,100)
    y=np.sin(x+i*0.3)

    plt.plot(x,y)
    plt.ylim(-2,2)

    fname=f"frame_{i}.png"
    plt.savefig(fname)
    plt.close()

    frames.append(imageio.imread(fname))

imageio.mimsave("results/gifs/walking.gif",frames,duration=0.1)