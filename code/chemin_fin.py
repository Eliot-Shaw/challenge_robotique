import math
import numpy as np
import sys
import chemin_base

# fonction enrée : faire_chemin(liste_cylindres, profondeur de cylindres à faire)



# descrption des types_cylindre de cylindres gain, masse
type_cylindre =[(1.0, 1.0),
                (2.0, 2.0),
                (3.0, 2.0)]

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

def echanger_cylindres(cylindres, id_cylindre, id_voulue):
    if id_cylindre != len(cylindres):
        temp = np.array(cylindres[id_cylindre])
        cylindres[id_cylindre] = cylindres[id_voulue]
        cylindres[id_voulue] = temp
    return cylindres

def faire_chemin(cylindres, depth):
    for i in range(depth):
        cylindres = echanger_cylindres(cylindres, i+1, choix_cylindre_suivant(i))
    return cylindres