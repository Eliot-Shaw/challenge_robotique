import sys
import numpy as np
from mcmc_class import Mcmc
from mvt_robot import faisable
from chemin_fin import faire_chemin

def importerMap():
    argc = len(sys.argv)
    if argc < 2:
        print("preciser le nom du fichier de donnees en argument...")
        exit()
    #lecture du fichier
    DataMap = np.loadtxt(sys.argv[1], dtype=float)
    return(DataMap)

def Soustraire(lst_cylindres, cylindres_total):

    cylindres = cylindres_total.copy()

    premier_cylindre = lst_cylindres[-1]

    for cylindre in lst_cylindres:
        np.delete(cylindres, cylindre[3])

    np.concatenate(cylindres, np.array([premier_cylindre]), axis = 0)

    return cylindres


def main():

    map = importerMap()
    nb_cylindre = len(map)


    min = 2
    max = nb_cylindre
    milieu = (min + max)// 2
    meilleur_chemin = Mcmc.process(milieu // 2)

    while min < max:
        if not faisable(meilleur_chemin):
            max = milieu
            milieu = (min + max) // 2

            meilleur_chemin = Mcmc.process(milieu)
        else:
            min = milieu
            milieu = (min + max) // 2
            meilleur_chemin = Mcmc.process(milieu)

    chemin_finale = faire_chemin(Soustraire(meilleur_chemin, map))

    return chemin_finale
    

