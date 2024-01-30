import math
import numpy as np
import sys
import matplotlib.pyplot as plt

# cylindre type_cylindre :  coox      cooy      type_cylindre
#                           1.7554    1.8713    3.0000

# descrption des types_cylindre de cylindres gain, masse
type_cylindre =[(1.0, 1.0),
                (2.0, 2.0),
                (3.0, 2.0)]

def recup_data_map():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = np.loadtxt(sys.argv[1], skiprows=1, dtype=float)
    return DataMap

def init_cylindres(donnees_map):
    global cylindres 
    cylindres = np.concatenate((np.array([[0.0, 0.0, 0.0]]), donnees_map), axis=0) # creations des cylindres avec le bot en 0.0 une cylindre aussi

def calcul_dist(id1, id2):
    distance_raw = math.sqrt((float(cylindres[id1][0]) - float(cylindres[id2][0]))**2 + (float(cylindres[id1][1]) - float(cylindres[id2][1]))**2)
    distance_valeur = distance_raw/type_cylindre[int(cylindres[id2][2])-1][0]
    distance_valeur_poids = distance_valeur*type_cylindre[int(cylindres[id2][2])-1][1]
    return distance_valeur_poids

def choix_cylindre_suivant(id_cylindre):
    distance_candidat = []
    for i in range(len(cylindres)):
        if i > id_cylindre:
            distance_candidat.append(calcul_dist(id_cylindre, i))
        else: 
            distance_candidat.append(999999)
    restultat = distance_candidat.index(min(distance_candidat))
    return restultat

def echanger_cylindres(id_cylindre, id_voulue):
    print("--------------------------------------------------------------")
    print(f"on cherche à échanger id{id_cylindre} et id{id_voulue}")
    print(f"on cherche à échanger {cylindres[id_cylindre]} {cylindres[id_voulue]}")
    print("--- cylindres avant :")
    print(cylindres)
    temp = cylindres[id_cylindre]
    cylindres[id_cylindre] = cylindres[id_voulue]
    cylindres[id_voulue] = temp
    print("--- cylindres après :")
    print(cylindres)
    return cylindres

def main():
    init_cylindres(recup_data_map())

    for i in range(len(cylindres)):
        echanger_cylindres(i, choix_cylindre_suivant(i))
    
    print(cylindres)
    
    
    tColorTab = {1:'red', 2:'green', 3:'blue'}
    dbRayon = 0.85
    #affichage des donnees de la carte
    x=recup_data_map()[:,0]
    y=recup_data_map()[:,1]
    t=recup_data_map()[:,2]
    n = len(x)
    fig = plt.figure(1)
    ax = fig.gca()
    for i in range(n):
        plt.plot(x[i],y[i],marker='+',color=tColorTab[int(t[i])])
        c1 = plt.Circle((x[i],y[i]), dbRayon,color=tColorTab[int(t[i])] )
        ax.add_patch(c1)
    

    for i in range(len(cylindres)):
        x=cylindres[:,0]
        y=cylindres[:,1]
        ax.annotate(i, (x[i],y[i]))
    plt.show()

if __name__ == '__main__':
    main()
