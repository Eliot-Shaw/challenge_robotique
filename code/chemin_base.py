import math
import numpy as np
import sys

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
    print(DataMap)

def init_cylindres(donnees_map):
    cylindres = [0.0,0.0,0.0] # creations des cylindres avec le bot en 0.0 une cylindre aussi
    cylindres.append(donnees_map)
    return cylindres 

def calcul_dist(cylindre1, cylindre2):
    distance_raw = math.sqrt((cylindre1[0] - cylindre2[0])**2 + (cylindre1[1] - cylindre2[1])**2)
    distance_valeur = distance_raw/type_cylindre[cylindre2[2]-1][0]
    distance_valeur_poids = distance_valeur*type_cylindre[cylindre2[2]-1][1]
    return distance_valeur_poids

def cylindre_plus_adapte(id_cylindre, cylindres):
    pass