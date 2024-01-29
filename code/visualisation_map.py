# utilitaire permettant de charger les donnees de la carte du
# challenge et de la visualiser
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

tColorTab = {1:'red', 2:'green', 3:'blue'}
dbRayon = 0.85
##########################
# point d'entree du script 
##########################
argc = len(sys.argv)
if argc < 2:
    print("preciser le nom du fichier de donnees en argument...")
    exit()
#lecture du fichier
DataMap = np.loadtxt(sys.argv[1], skiprows=1, dtype=float)
#affichage des donnees de la carte
x=DataMap[:,0]
y=DataMap[:,1]
t=DataMap[:,2]
n = len(x)
fig = plt.figure(1)
ax = fig.gca()
for i in range(n):
    plt.plot(x[i],y[i],marker='+',color=tColorTab[int(t[i])])
    c1 = plt.Circle((x[i],y[i]), dbRayon,color=tColorTab[int(t[i])] )
    ax.add_patch(c1)
plt.show()
