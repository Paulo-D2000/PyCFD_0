import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import subprocess

#Plot results ? (SLOW!!!!)
do_Plot = False

#Grid size
Lx = 12.8
Ly = 12.8

#Simulation time
T = 20

#Space step
dx = 0.05
dy = 0.05

#time step
dt = 1/30

#Static velocity
Vx = 0
Vy = -12.0

#total size
LenX = int(Lx/dx)
LenY = int(Lx/dx)
LenT = int(T/dt)

#arrays
Z = np.zeros((LenX,LenY))

#start plot
plt.ion()

#main time loop
for k in range(LenT):
   
    #add 10.0 units at the center
    Z[LenX-5][LenY//2] = 10.0

    #varying vx
    Vx = np.sin(k*0.06)*np.random.randint(1,4)*np.sin(k*0.1)
    
    #simulate
    for j in range(1,LenX-1,1):
        for i in range(1,LenY-1,1):
            #2D diffusion
            Z[j][i] = Z[j][i] + dx*((Z[j+1][i] - 2*Z[j][i] + Z[j-1][i])+(Z[j][i+1] - 2*Z[j][i] + Z[j][i-1]))
            #2D advection
            Z[j][i] += (((Z[j-1][i]- Z[j+1][i])*Vy) + ((Z[j][i-1]- Z[j][i+1])*Vx))*0.5*dt

    #plot each 15th timestep
    if(k%15 == 0):
        print("Simulation %f%% done. Image index: %d" % ((k/LenT)*100,k))
        if(do_Plot):
            plt.clf() 
            plt.figure(1)   
            plt.imshow(Z,interpolation='bilinear')  
            plt.show()
            plt.pause(0.01)
    #save frames as png
    im = Image.fromarray(np.uint8(cm.viridis(Z)*255))
    im = im.resize((480,480),Image.BILINEAR)
    im.save("out/cfd_%d.png"%(k))

#call ffmpeg to generate mp4 video
command = "ffmpeg -r 30 -i out/cfd_%d.png -c:v libx264 -pix_fmt yuv420p test.mp4"
subprocess.call(command)
